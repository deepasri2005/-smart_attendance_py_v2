"""
CCTV Blueprint Routes — Camera registry & detection stream processing
"""
from flask import Blueprint, render_template, request, jsonify, g, flash, redirect, url_for, abort
from app.decorators.auth import login_required
from app.services.auth_service import AuthService
from app.services.cctv_service import CCTVService
from app.models.attendance import CCTVCamera, CCTVDetectionLog

cctv_bp = Blueprint('cctv', __name__, url_prefix='/cctv')

@cctv_bp.route('/')
@login_required
def index():
    """CCTV camera management page."""
    user = g.current_user
    if not (user.is_super_admin or user.is_org_admin or user.is_emp_admin):
        abort(403)
    sidebar = AuthService.get_sidebar_menu(user)
    if user.is_super_admin:
        cameras = CCTVCamera.query.all()
        logs = CCTVDetectionLog.query.order_by(CCTVDetectionLog.id.desc()).limit(50).all()
    else:
        cameras = CCTVCamera.query.filter_by(organization_id=user.organization_id).all()
        logs = CCTVDetectionLog.query.filter_by(organization_id=user.organization_id).order_by(CCTVDetectionLog.id.desc()).limit(50).all()

    return render_template('cctv/index.html', user=user, sidebar=sidebar, cameras=cameras, logs=logs)


@cctv_bp.route('/api/add-camera', methods=['POST'])
@login_required
def api_add_camera():
    """Register a new CCTV camera."""
    user = g.current_user
    org_id = user.organization_id or 1

    data = request.get_json() or request.form
    name = data.get('name')
    location = data.get('camera_location')
    rtsp = data.get('rtsp_url')

    if not name:
        return jsonify({'success': False, 'message': 'Camera name is required'}), 400

    camera = CCTVService.register_camera(
        organization_id=org_id,
        name=name,
        camera_location=location,
        rtsp_url=rtsp
    )

    if request.is_json:
        return jsonify({'success': True, 'camera': camera.to_dict()})

    flash(f"Camera '{camera.name}' added successfully!", 'success')
    return redirect(url_for('cctv.index'))


@cctv_bp.route('/api/process-frame', methods=['POST'])
@login_required
def api_process_frame():
    """Process a single CCTV frame from frontend simulation or stream worker."""
    user = g.current_user
    org_id = user.organization_id or 1

    data = request.get_json() or {}
    camera_id = data.get('camera_id', 1)
    image_data = data.get('image')

    if not image_data:
        return jsonify({'success': False, 'message': 'Image frame required'}), 400

    res = CCTVService.process_camera_frame(
        organization_id=org_id,
        camera_id=camera_id,
        image_input=image_data
    )

    return jsonify({'success': True, 'data': res})
