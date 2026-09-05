"""
CCTV Service — Camera registry management & frame recognition processing
"""
from datetime import datetime, timedelta
from app.extensions import db
from app.models.attendance import CCTVCamera, CCTVDetectionLog
from app.models.employee import AttendanceRule
from app.services.face_service import FaceService
from app.services.attendance_service import AttendanceService

class CCTVService:
    """Manages CCTV cameras and automated video stream face processing."""

    @staticmethod
    def register_camera(organization_id: int, name: str, camera_location: str = None, rtsp_url: str = None):
        """Registers a new CCTV camera."""
        camera = CCTVCamera(
            organization_id=organization_id,
            name=name,
            camera_location=camera_location,
            rtsp_url=rtsp_url,
            status='ONLINE',
            is_active=True,
            last_heartbeat=datetime.utcnow()
        )
        db.session.add(camera)
        db.session.commit()
        return camera

    @staticmethod
    def process_camera_frame(organization_id: int, camera_id: int, image_input):
        """
        Processes a video frame from a CCTV camera stream.
        1. Performs face recognition against registered organization profiles.
        2. Logs the detection event in CCTVDetectionLog.
        3. Marks attendance if employee matched and cooldown window passed.
        """
        camera = db.session.get(CCTVCamera, camera_id)
        if camera:
            camera.last_heartbeat = datetime.utcnow()
            camera.status = 'ONLINE'

        user, confidence, msg = FaceService.recognize_face(organization_id, image_input)

        log = CCTVDetectionLog(
            organization_id=organization_id,
            camera_id=camera_id,
            user_id=user.id if user else None,
            confidence_score=confidence,
            attendance_marked=False,
            created_at=datetime.utcnow()
        )

        attendance_result = None
        if user and confidence >= 50.0:
            # Check CCTV cooldown period from organization attendance rules (default 30 mins)
            rule = AttendanceRule.query.filter_by(organization_id=organization_id).first()
            cooldown_mins = rule.cctv_cooldown_minutes if rule else 30

            recent_log = CCTVDetectionLog.query.filter(
                CCTVDetectionLog.organization_id == organization_id,
                CCTVDetectionLog.user_id == user.id,
                CCTVDetectionLog.attendance_marked == True,
                CCTVDetectionLog.detected_at >= datetime.utcnow() - timedelta(minutes=cooldown_mins)
            ).first()

            if not recent_log:
                action, att_dict, att_msg = AttendanceService.record_attendance(
                    organization_id=organization_id,
                    user_id=user.id,
                    method='CCTV',
                    confidence_score=confidence
                )
                log.attendance_marked = True
                attendance_result = {
                    'action': action,
                    'user': user.full_name,
                    'confidence': confidence,
                    'message': att_msg
                }

        db.session.add(log)
        db.session.commit()

        return {
            'matched': user is not None,
            'user': user.to_dict() if user else None,
            'confidence': confidence,
            'message': msg,
            'attendance': attendance_result
        }
