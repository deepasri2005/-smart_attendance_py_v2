"""
Face Recognition Service — OpenCV & NumPy computer vision processing
Detects faces, generates 128D feature encodings, matches faces, and registers profiles.
"""
import cv2
import numpy as np
import base64
import os
from datetime import datetime, date, time
from flask import current_app
from app.extensions import db
from app.models.attendance import FaceProfile, FaceEncoding, Attendance, AttendanceLog, CCTVDetectionLog
from app.models.user import User

# Load OpenCV Cascade Classifier if available in installed cv2 build
face_cascade = None
if hasattr(cv2, 'CascadeClassifier') and hasattr(cv2, 'data') and hasattr(cv2.data, 'haarcascades'):
    try:
        CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    except Exception:
        face_cascade = None

class FaceService:
    """Core Face Recognition & Verification Engine."""

    @staticmethod
    def decode_image(image_input):
        """Converts base64 string or file bytes into OpenCV BGR numpy array."""
        try:
            if isinstance(image_input, str):
                if ',' in image_input:
                    image_input = image_input.split(',')[1]
                img_data = base64.b64decode(image_input)
            else:
                img_data = image_input

            nparr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img
        except Exception as e:
            current_app.logger.error(f"Image decode error: {e}")
            return None

    @staticmethod
    def detect_face(img):
        """Detects the largest face bounding box in image. Returns (x, y, w, h) or center ROI."""
        if img is None or img.size == 0:
            return None
        
        if face_cascade is not None:
            try:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(60, 60)
                )
                if len(faces) > 0:
                    return max(faces, key=lambda rect: rect[2] * rect[3])
            except Exception:
                pass

        # Center region ROI fallback
        h, w = img.shape[:2]
        margin_w = int(w * 0.15)
        margin_h = int(h * 0.15)
        return (margin_w, margin_h, w - 2 * margin_w, h - 2 * margin_h)

    @staticmethod
    def compute_encoding(img, face_box=None):
        """
        Extracts a normalized 128D feature vector representation of the face region
        using OpenCV color/spatial normalization and histogram feature extraction.
        """
        if img is None:
            return None

        if face_box is not None:
            x, y, w, h = face_box
            face_roi = img[max(0, y):y+h, max(0, x):x+w]
        else:
            face_roi = img

        if face_roi.size == 0:
            return None

        # Resize to standard 128x128 resolution
        resized = cv2.resize(face_roi, (128, 128))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        equ = cv2.equalizeHist(gray)

        # Compute multi-scale grid histogram features to form 128D encoding
        grid_h, grid_w = 4, 4
        cell_h, cell_w = 128 // grid_h, 128 // grid_w
        features = []

        for i in range(grid_h):
            for j in range(grid_w):
                cell = equ[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
                hist = cv2.calcHist([cell], [0], None, [8], [0, 256])
                hist = hist.flatten()
                norm = np.linalg.norm(hist)
                if norm > 0:
                    hist = hist / norm
                features.extend(hist)

        encoding = np.array(features, dtype=np.float64)
        # Ensure 128 dimensions
        if len(encoding) > 128:
            encoding = encoding[:128]
        elif len(encoding) < 128:
            encoding = np.pad(encoding, (0, 128 - len(encoding)))

        # L2 Normalize final 128D vector
        norm = np.linalg.norm(encoding)
        if norm > 0:
            encoding = encoding / norm

        return encoding

    @staticmethod
    def compare_encodings(target_encoding, stored_encodings, tolerance=0.55):
        """
        Compares target encoding against a list of stored encodings.
        Returns (best_match_idx, confidence_score, is_match).
        """
        if target_encoding is None or not stored_encodings:
            return -1, 0.0, False

        distances = []
        for enc in stored_encodings:
            if enc is None or len(enc) != len(target_encoding):
                distances.append(1.0)
            else:
                # Cosine distance = 1 - dot_product
                dist = 1.0 - float(np.dot(target_encoding, enc))
                distances.append(max(0.0, dist))

        best_idx = int(np.argmin(distances))
        best_dist = distances[best_idx]
        confidence = round(max(0.0, (1.0 - best_dist)) * 100, 1)

        is_match = best_dist <= tolerance
        return best_idx, confidence, is_match

    @staticmethod
    def register_face_profile(organization_id: int, user_id: int, image_input, registered_by_id: int = None):
        """Registers or updates a face profile and encoding for a user."""
        img = FaceService.decode_image(image_input)
        if img is None:
            return False, "Invalid image format"

        face_box = FaceService.detect_face(img)
        if face_box is None:
            return False, "No clear face detected in image"

        encoding = FaceService.compute_encoding(img, face_box)
        if encoding is None:
            return False, "Failed to compute face features"

        # Check existing profile
        profile = FaceProfile.query.filter_by(organization_id=organization_id, user_id=user_id).first()
        if not profile:
            profile = FaceProfile(
                organization_id=organization_id,
                user_id=user_id,
                is_active=True,
                registered_by=registered_by_id
            )
            db.session.add(profile)
            db.session.flush()

        # Save encoding blob
        encoding_bytes = encoding.tobytes()
        enc_record = FaceEncoding(
            face_profile_id=profile.id,
            encoding_data=encoding_bytes,
            is_primary=True
        )
        db.session.add(enc_record)
        db.session.commit()

        return True, "Face profile registered successfully"

    @staticmethod
    def recognize_face(organization_id: int, image_input):
        """
        Matches an input image frame against all active employee face encodings in organization.
        Returns (user, confidence_score) or (None, 0.0).
        """
        img = FaceService.decode_image(image_input)
        if img is None:
            return None, 0.0, "Invalid image"

        face_box = FaceService.detect_face(img)
        if face_box is None:
            return None, 0.0, "No face detected"

        target_encoding = FaceService.compute_encoding(img, face_box)
        if target_encoding is None:
            return None, 0.0, "Encoding extraction failed"

        # Load all active profiles and primary encodings for organization
        profiles = FaceProfile.query.filter_by(organization_id=organization_id, is_active=True).all()
        if not profiles:
            return None, 0.0, "No registered face profiles found in organization"

        stored_encodings = []
        user_map = []

        for p in profiles:
            primary_enc = FaceEncoding.query.filter_by(face_profile_id=p.id).first()
            if primary_enc and primary_enc.encoding_data:
                try:
                    arr = np.frombuffer(primary_enc.encoding_data, dtype=np.float64)
                    if len(arr) == 128:
                        stored_encodings.append(arr)
                        user_map.append(p.user_id)
                except Exception:
                    continue

        if not stored_encodings:
            return None, 0.0, "No valid encodings stored"

        best_idx, confidence, is_match = FaceService.compare_encodings(target_encoding, stored_encodings)
        if is_match and best_idx < len(user_map):
            matched_user_id = user_map[best_idx]
            user = db.session.get(User, matched_user_id)
            return user, confidence, "Match found"

        return None, confidence, "Face unrecognized"
