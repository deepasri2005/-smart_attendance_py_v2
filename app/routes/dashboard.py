"""
Dashboard Routes Blueprint — role-specific dashboards
"""
from flask import Blueprint, render_template, jsonify, g
from flask_jwt_extended import get_jwt_identity
from datetime import date, timedelta
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError
from app.decorators.auth import login_required
from app.services.auth_service import AuthService
from app.models.employee import EmployeeProfile, Department
from app.models.attendance import Attendance
from app.models.leave import LeaveApplication
from app.models.notification import Notification
from app.models.organization import Organization
from app.models.user import User
from app.extensions import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    """Route to role-specific dashboard."""
    user = g.current_user
    sidebar = AuthService.get_sidebar_menu(user)
    today = date.today()

    if user.is_super_admin:
        stats = _get_super_admin_stats(today)
        return render_template('dashboard/super_admin.html',
                               user=user, sidebar=sidebar, stats=stats, today=today)

    elif user.is_org_admin:
        stats = _get_org_admin_stats(user.organization_id, today)
        return render_template('dashboard/org_admin.html',
                               user=user, sidebar=sidebar, stats=stats, today=today)

    elif user.is_emp_admin:
        stats = _get_org_admin_stats(user.organization_id, today)
        return render_template('dashboard/emp_admin.html',
                               user=user, sidebar=sidebar, stats=stats, today=today)

    else:
        # Employee
        stats = _get_employee_stats(user, today)
        return render_template('dashboard/employee.html',
                               user=user, sidebar=sidebar, stats=stats, today=today)


@dashboard_bp.route('/api/stats')
@login_required
def api_stats():
    """AJAX endpoint for dashboard stats refresh."""
    user = g.current_user
    today = date.today()

    if user.is_super_admin:
        return jsonify(_get_super_admin_stats(today))
    elif user.is_org_admin or user.is_emp_admin:
        return jsonify(_get_org_admin_stats(user.organization_id, today))
    else:
        return jsonify(_get_employee_stats(user, today))


# ─── Private helpers ──────────────────────────────────────────────────────────

def _get_super_admin_stats(today: date) -> dict:
    total_orgs = Organization.query.count()
    active_orgs = _safe_count(Organization.query.filter_by(is_active=True))
    total_employees = _safe_count(EmployeeProfile.query)

    present = _safe_count(db.session.query(func.count(Attendance.id)).filter(
        Attendance.attendance_date == today,
        Attendance.check_in.isnot(None)
    )) or 0

    on_leave = _safe_count(db.session.query(func.count(LeaveApplication.id)).filter(
        LeaveApplication.from_date <= today,
        LeaveApplication.to_date >= today,
        LeaveApplication.status == 'APPROVED'
    )) or 0

    pending_approvals = _safe_count(LeaveApplication.query.filter_by(status='PENDING'))

    return {
        'total_orgs': total_orgs,
        'active_orgs': active_orgs,
        'total_employees': total_employees,
        'present_today': present,
        'on_leave': on_leave,
        'absent_today': max(0, total_employees - present - on_leave),
        'pending_approvals': pending_approvals,
    }


def _get_org_admin_stats(org_id: int, today: date) -> dict:
    total_employees = _safe_count(EmployeeProfile.query.filter_by(organization_id=org_id))

    present = _safe_count(db.session.query(func.count(Attendance.id)).filter(
        Attendance.organization_id == org_id,
        Attendance.attendance_date == today,
        Attendance.check_in.isnot(None)
    )) or 0

    on_leave = _safe_count(db.session.query(func.count(LeaveApplication.id)).filter(
        LeaveApplication.organization_id == org_id,
        LeaveApplication.from_date <= today,
        LeaveApplication.to_date >= today,
        LeaveApplication.status == 'APPROVED'
    )) or 0

    late = _safe_count(db.session.query(func.count(Attendance.id)).filter(
        Attendance.organization_id == org_id,
        Attendance.attendance_date == today,
        Attendance.is_late == True
    )) or 0

    pending = _safe_count(LeaveApplication.query.filter_by(
        organization_id=org_id, status='PENDING'
    ))

    return {
        'total_employees': total_employees,
        'present_today': present,
        'absent_today': max(0, total_employees - present - on_leave),
        'late_today': late,
        'on_leave': on_leave,
        'pending_approvals': pending,
    }


def _get_employee_stats(user: User, today: date) -> dict:
    attendance = Attendance.query.filter_by(
        user_id=user.id, attendance_date=today
    ).first()

    first_of_month = today.replace(day=1)
    month_attendance = Attendance.query.filter(
        Attendance.user_id == user.id,
        Attendance.attendance_date >= first_of_month,
        Attendance.attendance_date <= today,
    ).all()

    present_days = sum(1 for a in month_attendance if a.check_in is not None)
    late_days = sum(1 for a in month_attendance if a.is_late)

    pending_leaves = LeaveApplication.query.filter_by(
        user_id=user.id, status='PENDING'
    ).count()

    unread_notifications = Notification.query.filter_by(
        user_id=user.id, is_read=False
    ).count()

    return {
        'today_attendance': attendance.to_dict() if attendance else None,
        'present_days_this_month': present_days,
        'late_days_this_month': late_days,
        'pending_leaves': pending_leaves,
        'unread_notifications': unread_notifications,
    }


def _safe_count(query) -> int:
    """Return zero when an optional legacy table is absent from the database."""
    try:
        return query.count()
    except SQLAlchemyError:
        db.session.rollback()
        return 0
