"""Protected landing pages for the registered module catalog."""
from flask import Blueprint, abort, g, render_template
from app.extensions import db
from app.decorators.auth import login_required, permission_required
from app.modules import get_module
from app.services.auth_service import AuthService

module_pages_bp = Blueprint('module_pages', __name__, url_prefix='/modules')


def _feature(slug, feature_slug):
    module = get_module(slug)
    if not module:
        abort(404)
    feature = next((item for item in module['features'] if item['slug'] == feature_slug), None)
    if not feature:
        abort(404)
    return module, feature


def _filter_module_features_for_user(module, user):
    if user.is_super_admin or not module:
        return module
    mod_copy = dict(module)
    filtered_features = [
        feat for feat in module.get('features', [])
        if AuthService.check_permission(user.id, module['slug'], 'view', feat['slug'])
    ]
    mod_copy['features'] = filtered_features
    return mod_copy


@module_pages_bp.get('/<slug>')
@login_required
def module_index(slug):
    module = get_module(slug)
    if not module:
        abort(404)
    
    user = g.current_user
    if not user.is_super_admin and not AuthService.has_module_access(user.id, slug):
        abort(403)

    sidebar = AuthService.get_sidebar_menu(user)
    ctx = _get_module_context(slug, user)
    filtered_module = _filter_module_features_for_user(module, user)
    
    return render_template(
        'modules/feature.html',
        user=user,
        sidebar=sidebar,
        module=filtered_module,
        feature=None,
        **ctx
    )


@module_pages_bp.get('/<slug>/<feature_slug>')
@login_required
def feature_index(slug, feature_slug):
    module, feature = _feature(slug, feature_slug)
    user = g.current_user
    
    if not user.is_super_admin and (
        not AuthService.has_module_access(user.id, slug) or
        not AuthService.check_permission(user.id, slug, 'view', feature_slug)
    ):
        abort(403)
        
    sidebar = AuthService.get_sidebar_menu(user)
    norm_feature = feature_slug.lower().replace('-', '_')

    # Dedicated interactive view for Face Attendance
    if (slug in ('attendance', 'face_ai')) and norm_feature in ('face_attendance', 'face', 'face_ai', 'enrollment'):
        from datetime import date
        from app.models.attendance import Attendance, FaceProfile
        from app.models.user import User

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

    # Dedicated interactive view for CCTV Attendance
    if (slug in ('attendance', 'cctv')) and norm_feature in ('cctv_attendance', 'cctv', 'live_stream', 'camera_management'):
        from app.models.attendance import CCTVCamera, CCTVDetectionLog
        if user.is_super_admin:
            cameras = CCTVCamera.query.filter_by(is_active=True).all()
            recent_logs = CCTVDetectionLog.query.order_by(CCTVDetectionLog.id.desc()).limit(20).all()
        else:
            cameras = CCTVCamera.query.filter_by(organization_id=user.organization_id, is_active=True).all()
            recent_logs = CCTVDetectionLog.query.filter_by(organization_id=user.organization_id).order_by(CCTVDetectionLog.id.desc()).limit(20).all()

        return render_template(
            'attendance/cctv_attendance.html',
            user=user,
            sidebar=sidebar,
            cameras=cameras,
            recent_logs=recent_logs
        )

    ctx = _get_module_context(slug, user)

    return render_template(
        'modules/feature.html',
        user=user,
        sidebar=sidebar,
        module=module,
        feature=feature,
        **ctx
    )


def _get_module_context(slug, user):
    """Retrieve database records relevant to the current module page."""
    ctx = {}
    try:
        if slug in ('employees', 'employee'):
            from app.models.user import User
            from app.models.employee import EmployeeProfile, Department, Designation
            if user.is_super_admin:
                ctx['employees_list'] = User.query.all()
                ctx['departments'] = Department.query.all()
                ctx['designations'] = Designation.query.all()
            else:
                ctx['employees_list'] = User.query.filter_by(organization_id=user.organization_id).all()
                ctx['departments'] = Department.query.filter_by(organization_id=user.organization_id).all()
                ctx['designations'] = Designation.query.filter_by(organization_id=user.organization_id).all()

        elif slug in ('users_access', 'security'):
            from app.models.user import User
            from app.models.role import Role
            ctx['users_list'] = User.query.all() if user.is_super_admin else User.query.filter_by(organization_id=user.organization_id).all()
            ctx['roles'] = Role.query.all()

        elif slug == 'organization':
            from app.models.organization import Organization
            from app.models.employee import Department, Designation, OrganizationLocation, Holiday, WeekOffRule, AttendanceRule
            
            if user.is_super_admin:
                ctx['organizations'] = Organization.query.all()
                ctx['departments'] = Department.query.all()
                ctx['designations'] = Designation.query.all()
                ctx['locations'] = OrganizationLocation.query.all()
                ctx['holidays'] = Holiday.query.all()
                ctx['week_off_rules'] = WeekOffRule.query.all()
                ctx['attendance_rules'] = AttendanceRule.query.all()
            else:
                org_id = user.organization_id
                ctx['organizations'] = Organization.query.filter_by(id=org_id).all()
                ctx['departments'] = Department.query.filter_by(organization_id=org_id).all()
                ctx['designations'] = Designation.query.filter_by(organization_id=org_id).all()
                ctx['locations'] = OrganizationLocation.query.filter_by(organization_id=org_id).all()
                ctx['holidays'] = Holiday.query.filter_by(organization_id=org_id).all()
                ctx['week_off_rules'] = WeekOffRule.query.filter_by(organization_id=org_id).all()
                ctx['attendance_rules'] = AttendanceRule.query.filter_by(organization_id=org_id).all()
            
            # Active current organization context
            current_org_id = user.organization_id if not user.is_super_admin else (Organization.query.first().id if Organization.query.first() else 1)
            ctx['current_org'] = db.session.get(Organization, current_org_id) if current_org_id else None
            ctx['attendance_rule'] = AttendanceRule.query.filter_by(organization_id=current_org_id).first() if current_org_id else None

        elif slug == 'shifts':
            from app.models.employee import Shift
            ctx['shifts_list'] = Shift.query.all() if user.is_super_admin else Shift.query.filter_by(organization_id=user.organization_id).all()

        elif slug in ('leave', 'approvals'):
            from app.models.leave import LeaveApplication, LeaveType
            if user.is_super_admin:
                ctx['leave_applications'] = LeaveApplication.query.order_by(LeaveApplication.id.desc()).all()
                ctx['leave_types'] = LeaveType.query.all()
            else:
                ctx['leave_applications'] = LeaveApplication.query.filter_by(organization_id=user.organization_id).order_by(LeaveApplication.id.desc()).all()
                ctx['leave_types'] = LeaveType.query.filter_by(organization_id=user.organization_id).all()

        elif slug == 'geo_attendance':
            from app.models.employee import OrganizationLocation
            ctx['locations'] = OrganizationLocation.query.all() if user.is_super_admin else OrganizationLocation.query.filter_by(organization_id=user.organization_id).all()

        elif slug in ('audit_logs', 'notifications', 'reports', 'payroll'):
            from app.models.attendance import AttendanceLog, Attendance
            from datetime import date
            today = date.today()
            ctx['logs'] = AttendanceLog.query.order_by(AttendanceLog.id.desc()).limit(30).all()
            ctx['attendance_today'] = Attendance.query.filter_by(attendance_date=today).all()

    except Exception as e:
        print('Context loading warning:', e)

    return ctx
