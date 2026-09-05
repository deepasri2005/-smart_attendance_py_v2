"""
Models package — import all models here so Flask-Migrate
can discover them for schema generation.
"""
from app.models.organization import Organization
from app.models.role import Role, Module, SubModule, Permission, RolePermission, UserPermission
from app.models.user import User, LoginDetails, RefreshToken, TokenBlocklist, LoginHistory, DeviceRegistration
from app.models.employee import (
    Department, Designation, EmployeeProfile,
    Shift, EmployeeShift, OrganizationLocation,
    AttendanceRule, Holiday, WeekOffRule
)
from app.models.attendance import (
    Attendance, AttendanceLog, AttendanceRegularization,
    FaceProfile, FaceEncoding,
    CCTVCamera, CCTVDetectionLog, AttendanceAnomaly
)
from app.models.leave import LeaveType, LeaveBalance, LeaveApplication
from app.models.tour import TourApplication
from app.models.work_from_home import WFHApplication
from app.models.notification import Notification
from app.models.audit_log import AuditLog

__all__ = [
    'Organization',
    'Role', 'Module', 'SubModule', 'Permission', 'RolePermission', 'UserPermission',
    'User', 'LoginDetails', 'RefreshToken', 'TokenBlocklist', 'LoginHistory', 'DeviceRegistration',
    'Department', 'Designation', 'EmployeeProfile',
    'Shift', 'EmployeeShift', 'OrganizationLocation',
    'AttendanceRule', 'Holiday', 'WeekOffRule',
    'Attendance', 'AttendanceLog', 'AttendanceRegularization',
    'FaceProfile', 'FaceEncoding',
    'CCTVCamera', 'CCTVDetectionLog', 'AttendanceAnomaly',
    'LeaveType', 'LeaveBalance', 'LeaveApplication',
    'TourApplication',
    'WFHApplication',
    'Notification',
    'AuditLog',
]
