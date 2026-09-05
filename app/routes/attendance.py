"""
Attendance Blueprint Routes — Face Attendance, CCTV Monitoring, Geo, Manual
"""
from flask import Blueprint, render_template, request, jsonify, g, flash, redirect, url_for
from datetime import date, datetime
from app.decorators.auth import login_required
from app.services.auth_service import AuthService
from app.services.face_service import FaceService
from app.services.attendance_service import AttendanceService
from app.models.attendance import Attendance, FaceProfile, CCTVCamera, CCTVDetectionLog
from app.models.user import User

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@attendance_bp.route('/')
@login_required
def index():
    """Attendance summary & daily log view."""
    user = g.current_user
    sidebar = AuthService.get_sidebar_menu(user)
    today = date.today()

    if user.is_super_admin:
        records = Attendance.query.filter_by(attendance_date=today).all()
    else:
        records = Attendance.query.filter_by(organization_id=user.organization_id, attendance_date=today).all()

    return render_template('attendance/index.html', user=user, sidebar=sidebar, records=records, today=today)


@attendance_bp.route('/face')
@login_required
def face():
    """Interactive Live Webcam Face Attendance Scanner UI."""
    user = g.current_user
    sidebar = AuthService.get_sidebar_menu(user)
    today = date.today()

    if user.is_super_admin:
        all_users = User.query.filter_by(is_active=True).all()
        today_records = Attendance.query.filter_by(attendance_date=today).order_by(Attendance.id.desc()).all()
        registered_profiles = FaceProfile.query.filter_by(is_active=True).all()
    else:
        all_users = User.query.filter_by(organization_id=user.organization_id, is_active=True).all()
        today_records = Attendance.query.filter_by(organization_id=user.organization_id, attendance_date=today).order_by(Attendance.id.desc()).all()
        registered_profiles = FaceProfile.query.filter_by(organization_id=user.organization_id, is_active=True).all()

    return render_template(
        'attendance/face.html',
        user=user,
        sidebar=sidebar,
        all_users=all_users,
        today_records=today_records,
        registered_count=len(registered_profiles),
        total_users=len(all_users)
    )


@attendance_bp.route('/cctv')
@login_required
def cctv():
    """Live CCTV Attendance Monitoring Dashboard UI."""
    user = g.current_user
    if not (user.is_super_admin or user.is_org_admin or user.is_emp_admin):
        from flask import abort
        abort(403)
    sidebar = AuthService.get_sidebar_menu(user)
    if user.is_super_admin:
        cameras = CCTVCamera.query.filter_by(is_active=True).all()
        recent_logs = CCTVDetectionLog.query.order_by(CCTVDetectionLog.id.desc()).limit(20).all()
    else:
        cameras = CCTVCamera.query.filter_by(organization_id=user.organization_id, is_active=True).all()
        recent_logs = CCTVDetectionLog.query.filter_by(organization_id=user.organization_id).order_by(CCTVDetectionLog.id.desc()).limit(20).all()

    return render_template('attendance/cctv_attendance.html', user=user, sidebar=sidebar, cameras=cameras, recent_logs=recent_logs)


@attendance_bp.route('/api/face-checkin', methods=['POST'])
@login_required
def api_face_checkin():
    """
    API endpoint for real-time camera check-in / check-out.
    Accepts JSON with { "image": "data:image/jpeg;base64,..." }
    """
    user = g.current_user
    org_id = user.organization_id or 1

    data = request.get_json() or {}
    image_data = data.get('image')
    if not image_data:
        return jsonify({'success': False, 'message': 'Image frame is required'}), 400

    # Recognize face frame
    matched_user, confidence, msg = FaceService.recognize_face(org_id, image_data)
    if not matched_user:
        return jsonify({'success': False, 'message': msg, 'confidence': confidence}), 400

    # Record check-in or check-out
    action, att_dict, att_msg = AttendanceService.record_attendance(
        organization_id=org_id,
        user_id=matched_user.id,
        method='FACE',
        confidence_score=confidence,
        ip_address=request.remote_addr
    )

    return jsonify({
        'success': True,
        'action': action,
        'message': att_msg,
        'confidence': confidence,
        'user': matched_user.to_dict(),
        'attendance': att_dict
    }), 200


@attendance_bp.route('/api/register-face', methods=['POST'])
@login_required
def api_register_face():
    """API endpoint to register/store face encoding for a user."""
    user = g.current_user
    org_id = user.organization_id or 1

    data = request.get_json() or {}
    target_user_id = data.get('user_id', user.id)
    image_data = data.get('image')

    if not image_data:
        return jsonify({'success': False, 'message': 'Image is required'}), 400

    success, msg = FaceService.register_face_profile(
        organization_id=org_id,
        user_id=target_user_id,
        image_input=image_data,
        registered_by_id=user.id
    )

    if not success:
        return jsonify({'success': False, 'message': msg}), 400

    return jsonify({'success': True, 'message': msg}), 200
