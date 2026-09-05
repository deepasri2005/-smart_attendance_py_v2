"""
Authentication & Permission Decorators
"""
import functools
from flask import redirect, url_for, flash, request, jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User, TokenBlocklist
from app.extensions import db


def login_required(f):
    """
    Decorator that requires a valid JWT (from cookie or header).
    For HTML routes: redirects to login on failure.
    For API routes (JSON): returns 401 JSON.
    """
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        try:
            try:
                verify_jwt_in_request(optional=False)
            except Exception as jwt_err:
                try:
                    verify_jwt_in_request(optional=False, locations=['cookies', 'headers'], refresh=False)
                except Exception:
                    raise jwt_err

            jwt_data = get_jwt()

            # Check token is not blacklisted
            jti = jwt_data.get('jti')
            try:
                token_revoked = bool(
                    jti and db.session.query(TokenBlocklist).filter_by(jti=jti).first()
                )
            except SQLAlchemyError:
                db.session.rollback()
                token_revoked = False

            if token_revoked:
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({'success': False, 'message': 'Token revoked'}), 401
                return redirect(url_for('auth.login'))

            # Load user into g
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)
            if not user or not user.is_active:
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({'success': False, 'message': 'User inactive or not found'}), 401
                return redirect(url_for('auth.login'))

            g.current_user = user
            g.jwt_data = jwt_data
            return f(*args, **kwargs)

        except Exception as err:
            import traceback
            from flask import current_app
            current_app.logger.warning(f"Auth verification failed: {err}\n{traceback.format_exc()}")
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'success': False, 'message': f'Authentication required ({err})'}), 401
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login'))

    return decorated


def role_required(*roles):
    """
    Decorator that restricts access to specific roles.
    Usage: @role_required('SUPER_ADMIN', 'ORG_ADMIN')
    """
    def decorator(f):
        @functools.wraps(f)
        @login_required
        def decorated(*args, **kwargs):
            user = g.current_user
            if user.role_name not in roles:
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({'success': False, 'message': 'Insufficient permissions'}), 403
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard.index'))
            return f(*args, **kwargs)
        return decorated
    return decorator


def permission_required(module_slug, permission_name, sub_module_slug=None):
    """
    Decorator that checks dynamic RBAC permissions.
    Usage: @permission_required('attendance', 'approve')
           @permission_required('attendance', 'view', 'face_attendance')
    """
    def decorator(f):
        @functools.wraps(f)
        @login_required
        def decorated(*args, **kwargs):
            from app.services.auth_service import AuthService
            user = g.current_user

            # Super admin bypasses all permission checks
            if user.is_super_admin:
                return f(*args, **kwargs)

            has_perm = AuthService.check_permission(
                user_id=user.id,
                module_slug=module_slug,
                permission_name=permission_name,
                sub_module_slug=sub_module_slug
            )

            if not has_perm:
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({
                        'success': False,
                        'message': f'Permission denied: {permission_name} on {module_slug}'
                    }), 403
                flash('You do not have permission to perform this action.', 'danger')
                return redirect(url_for('dashboard.index'))

            return f(*args, **kwargs)
        return decorated
    return decorator


def module_required(module_slug):
    """
    Decorator that checks if user has any access to a module.
    Usage: @module_required('attendance')
    """
    def decorator(f):
        @functools.wraps(f)
        @login_required
        def decorated(*args, **kwargs):
            from app.services.auth_service import AuthService
            user = g.current_user

            if user.is_super_admin:
                return f(*args, **kwargs)

            has_access = AuthService.has_module_access(user.id, module_slug)
            if not has_access:
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({'success': False, 'message': 'Module access denied'}), 403
                flash('You do not have access to this module.', 'danger')
                return redirect(url_for('dashboard.index'))

            return f(*args, **kwargs)
        return decorated
    return decorator


def same_org_required(f):
    """
    Decorator that ensures users can only access their own organization's data.
    Stores org_id in g for route use.
    """
    @functools.wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        user = g.current_user
        if not user.is_super_admin:
            g.org_id = user.organization_id
        else:
            # Super admin can optionally filter by org via query param
            g.org_id = request.args.get('org_id', type=int)
        return f(*args, **kwargs)
    return decorated
