"""
Authentication Service — login, JWT, token management, permissions
"""
from datetime import datetime, timedelta
from flask import current_app, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt
)
from app.extensions import db
from app.models.user import User, LoginDetails, LoginHistory, TokenBlocklist, RefreshToken
from app.models.role import Role, RolePermission, UserPermission, Module, SubModule, Permission
from app.models.audit_log import AuditLog

SIDEBAR_MODULE_NAMES = {
    'organization': 'Organization',
    'users-access': 'Users & Access',
    'employees': 'Employees',
    'attendance': 'Attendance',
    'face-ai': 'Face AI',
    'cctv': 'CCTV',
    'geo-attendance': 'Geo Attendance',
    'shifts': 'Shifts',
    'leave': 'Leave',
    'tour': 'Tour',
    'work-from-home': 'Work From Home',
    'approvals': 'Approvals',
    'notifications': 'Notifications',
    'reports': 'Reports',
    'security': 'Security',
    'audit-logs': 'Audit Logs',
    'settings': 'Settings',
}

SIDEBAR_MODULES = {
    'dashboard', 'organization', 'users-access', 'employees', 'attendance',
    'face-ai', 'cctv', 'geo-attendance', 'shifts', 'leave', 'tour',
    'work-from-home', 'approvals', 'notifications', 'reports', 'security',
    'audit-logs', 'settings',
}

SIDEBAR_FEATURE_NAMES = {
    ('organization', 'Organization Profile'): 'Profile',
    ('organization', 'Department Management'): 'Departments',
    ('organization', 'Designation Management'): 'Designations',
    ('organization', 'Organization Locations'): 'Locations',
    ('organization', 'Holiday Management'): 'Holidays',
    ('organization', 'Week-Off Management'): 'Week-Off',
    ('organization', 'Organization Policies'): 'Attendance Rules',
    ('users-access', 'Login Details'): 'Login Details',
    ('employees', 'Employee Face Registration'): 'Face Registration',
    ('employees', 'Employee Shift Assignment'): 'Shift Assignment',
    ('attendance', 'Attendance Dashboard'): 'Dashboard',
    ('attendance', 'Attendance Regularization'): 'Regularization',
    ('attendance', 'Attendance Approval'): 'Approval',
    ('attendance', 'Attendance Anomalies'): 'Anomalies',
    ('face-ai', 'Face Profile Management'): 'Face Profiles',
    ('face-ai', 'Face Encoding Management'): 'Face Encodings',
    ('face-ai', 'Face Recognition Logs'): 'Recognition Logs',
    ('face-ai', 'Unknown Face Detection'): 'Unknown Faces',
    ('cctv', 'CCTV Camera List'): 'Cameras',
    ('cctv', 'Live Camera Monitoring'): 'Live Monitoring',
    ('cctv', 'CCTV Detection Logs'): 'Detection Logs',
    ('cctv', 'CCTV Processing Settings'): 'CCTV Settings',
    ('shifts', 'Shift Settings'): 'Shift Rules',
    ('shifts', 'Employee Shift Assignment'): 'Employee Shifts',
    ('leave', 'My Leave Applications'): 'My Applications',
    ('tour', 'My Tour Applications'): 'My Tours',
    ('work-from-home', 'Apply Work From Home'): 'Apply WFH',
    ('work-from-home', 'My WFH Applications'): 'My Requests',
    ('work-from-home', 'Daily Work Report'): 'Daily Work Report',
    ('approvals', 'Pending Approvals'): 'Pending Requests',
    ('approvals', 'Attendance Approvals'): 'Attendance',
    ('approvals', 'Leave Approvals'): 'Leave',
    ('approvals', 'Tour Approvals'): 'Tour',
    ('approvals', 'WFH Approvals'): 'Work From Home',
    ('notifications', 'Announcement Management'): 'Announcements',
    ('notifications', 'Notification Templates'): 'Templates',
    ('reports', 'Analytics Dashboard'): 'Analytics',
    ('security', 'Registered Devices'): 'Devices',
}


class AuthService:
    """Handles all authentication and authorization logic."""

    @staticmethod
    def login(username: str, password: str, ip_address: str = None, user_agent: str = None):
        """
        Authenticates a user by username and password.
        Returns (success, data/error_message).
        """
        login_details = LoginDetails.query.filter_by(username=username).first()

        # Log the attempt regardless of outcome
        history = LoginHistory(
            username_attempted=username,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        if not login_details or not login_details.is_active:
            history.status = 'FAILED'
            db.session.add(history)
            db.session.commit()
            return False, 'Invalid username or password'

        # Check account lockout
        if login_details.is_locked():
            history.user_id = login_details.user_id
            history.status = 'LOCKED'
            db.session.add(history)
            db.session.commit()
            return False, 'Account is temporarily locked due to too many failed attempts'

        # Verify password
        if not login_details.check_password(password):
            login_details.failed_attempts += 1
            max_attempts = current_app.config.get('LOGIN_MAX_ATTEMPTS', 5)
            lockout_minutes = current_app.config.get('LOGIN_LOCKOUT_MINUTES', 15)

            if login_details.failed_attempts >= max_attempts:
                login_details.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)

            history.user_id = login_details.user_id
            history.status = 'FAILED'
            db.session.add(history)
            db.session.commit()
            return False, 'Invalid username or password'

        user = db.session.get(User, login_details.user_id)
        if not user or not user.is_active:
            history.status = 'FAILED'
            db.session.add(history)
            db.session.commit()
            return False, 'Account is inactive'

        # Successful login — reset failed attempts
        login_details.failed_attempts = 0
        login_details.locked_until = None
        login_details.last_login = datetime.utcnow()

        # Load permissions
        modules, sub_modules = AuthService._get_user_permissions(user)

        # Build JWT claims
        additional_claims = {
            'username': login_details.username,
            'email': user.email,
            'mobile_number': login_details.mobile_number,
            'role': user.role_name,
            'organization_id': user.organization_id,
        }

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(identity=str(user.id))

        # Audit log
        audit = AuditLog(
            organization_id=user.organization_id,
            user_id=user.id,
            action='LOGIN',
            module='auth',
            new_data={'description': f'User {username} logged in successfully'},
            ip_address=ip_address,
            user_agent=user_agent,
        )

        history.user_id = user.id
        history.status = 'SUCCESS'

        db.session.add(history)
        db.session.add(audit)
        db.session.commit()

        return True, {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(),
            'permissions': {
                'modules': modules,
                'sub_modules': sub_modules,
                'sidebar': AuthService.get_sidebar_menu(user),
            }
        }

    @staticmethod
    def logout(jti: str, user_id: int, expires_at: datetime):
        """Blacklist the current JWT token."""
        blocklist = TokenBlocklist(
            jti=jti,
            token_type='access',
            user_id=user_id,
            expires_at=expires_at,
        )
        audit = AuditLog(
            user_id=user_id,
            action='LOGOUT',
            module='auth',
            new_data={'description': 'User logged out'},
            ip_address=request.remote_addr if request else None,
        )
        db.session.add(blocklist)
        db.session.add(audit)
        db.session.commit()

    @staticmethod
    def revoke_token(jti: str):
        """Check if a token's JTI is in the blocklist."""
        return db.session.query(TokenBlocklist).filter_by(jti=jti).first() is not None

    @staticmethod
    def _get_user_permissions(user: User):
        """
        Returns (modules_list, sub_modules_list) based on role permissions
        and any user-level overrides.
        """
        if user.is_super_admin:
            # Super admin gets all modules
            all_modules = Module.query.filter_by(is_active=True).all()
            all_sub = SubModule.query.filter_by(is_active=True).all()
            return [m.slug for m in all_modules], [s.slug for s in all_sub]

        # Get role-level permissions
        role_perms = RolePermission.query.filter_by(role_id=user.role_id).all()
        modules_set = set()
        sub_modules_set = set()

        for rp in role_perms:
            if rp.module:
                modules_set.add(rp.module.slug)
            if rp.sub_module:
                sub_modules_set.add(rp.sub_module.slug)

        # Apply user-level overrides
        user_perms = UserPermission.query.filter_by(user_id=user.id).all()
        for up in user_perms:
            if up.is_granted:
                if up.module:
                    modules_set.add(up.module.slug)
                if up.sub_module:
                    sub_modules_set.add(up.sub_module.slug)
            else:
                # Explicit deny
                if up.module:
                    modules_set.discard(up.module.slug)
                if up.sub_module:
                    sub_modules_set.discard(up.sub_module.slug)

        return list(modules_set), list(sub_modules_set)

    @staticmethod
    def check_permission(user_id: int, module_slug: str, permission_name: str,
                         sub_module_slug: str = None) -> bool:
        """Check if user has a specific permission on a module/sub-module."""
        user = db.session.get(User, user_id)
        if not user:
            return False

        if user.is_super_admin:
            return True

        module = Module.query.filter_by(slug=module_slug).first()
        if not module:
            return False

        permission = Permission.query.filter_by(name=permission_name).first()
        if not permission:
            return False

        sub_module = None
        if sub_module_slug:
            sub_module = SubModule.query.filter_by(slug=sub_module_slug, module_id=module.id).first()

        # Check role permission
        query = RolePermission.query.filter_by(
            role_id=user.role_id,
            module_id=module.id,
            permission_id=permission.id,
        )
        if sub_module:
            query = query.filter_by(sub_module_id=sub_module.id)
        else:
            query = query.filter_by(sub_module_id=None)

        role_perm = query.first()

        # Check user-level override
        u_query = UserPermission.query.filter_by(
            user_id=user_id,
            module_id=module.id,
            permission_id=permission.id,
        )
        if sub_module:
            u_query = u_query.filter_by(sub_module_id=sub_module.id)
        user_perm = u_query.first()

        if user_perm:
            return user_perm.is_granted

        return role_perm is not None

    @staticmethod
    def has_module_access(user_id: int, module_slug: str) -> bool:
        """Check if user has any access to a module."""
        user = db.session.get(User, user_id)
        if not user:
            return False
        if user.is_super_admin:
            return True

        module = Module.query.filter_by(slug=module_slug).first()
        if not module:
            return False

        rp = RolePermission.query.filter_by(
            role_id=user.role_id,
            module_id=module.id,
        ).first()
        return rp is not None

    @staticmethod
    def get_sidebar_menu(user: User) -> list:
        """
        Returns the sidebar navigation structure for a user
        based on their permissions.
        """
        from app.modules import get_module

        if user.is_super_admin:
            modules = Module.query.filter_by(is_active=True).order_by(Module.order).all()
            module_ids = {module.id for module in modules}
            sub_module_ids = None
        else:
            role_perms = RolePermission.query.filter_by(role_id=user.role_id).all()
            module_ids = {rp.module_id for rp in role_perms}
            sub_module_ids = {rp.sub_module_id for rp in role_perms if rp.sub_module_id}

            # User-level grants add access; explicit denies remove it.
            for user_perm in UserPermission.query.filter_by(user_id=user.id).all():
                if user_perm.is_granted:
                    module_ids.add(user_perm.module_id)
                    if user_perm.sub_module_id:
                        sub_module_ids.add(user_perm.sub_module_id)
                else:
                    module_ids.discard(user_perm.module_id)
                    if user_perm.sub_module_id:
                        sub_module_ids.discard(user_perm.sub_module_id)

            modules = Module.query.filter(
                Module.id.in_(module_ids),
                Module.is_active == True
            ).order_by(Module.order).all()

        menu = []
        for module in modules:
            if module.slug not in SIDEBAR_MODULES:
                continue
            definition = get_module(module.slug)
            sidebar_names = {
                feature['name'] for feature in (definition or {}).get('features', [])
                if feature.get('sidebar')
            }
            sub_query = SubModule.query.filter_by(module_id=module.id, is_active=True)
            if module.slug in ('dashboard', 'audit-logs'):
                subs = []
            else:
                subs = [sub for sub in sub_query.order_by(SubModule.order).all()
                        if sub.name in sidebar_names and (
                            sub_module_ids is None or sub.id in sub_module_ids
                        )]

            menu.append({
                'name': SIDEBAR_MODULE_NAMES.get(module.slug, module.name),
                'slug': module.slug,
                'icon': module.icon,
                'route': module.route,
                'sub_modules': [
                    {
                        **sub.to_dict(),
                        'name': SIDEBAR_FEATURE_NAMES.get((module.slug, sub.name), sub.name),
                    }
                    for sub in subs
                ],
            })

        return menu
