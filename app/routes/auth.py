"""
Auth Routes Blueprint — login, logout, refresh token, forgot password
"""
from datetime import datetime, timezone
from flask import (
    Blueprint, render_template, redirect, url_for,
    request, flash, jsonify, make_response, g
)
from flask_jwt_extended import (
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies, get_jwt, get_jwt_identity,
    verify_jwt_in_request, create_access_token
)
from app.services.auth_service import AuthService
from app.models.user import TokenBlocklist
from app.extensions import db, limiter

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/')
def home():
    """Public home / landing page."""
    return redirect(url_for('main.home'))


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    """Login page — GET shows form, POST authenticates."""
    # Redirect existing sessions only when displaying the login page. A stale
    # browser cookie must not prevent a submitted credential from being tested.
    if request.method == 'GET':
        try:
            verify_jwt_in_request(optional=True)
            identity = get_jwt_identity()
            if identity:
                return redirect(url_for('dashboard.index'))
        except Exception:
            pass

    if request.method == 'POST':
        # Support both JSON (API) and form (web)
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Username and password are required'}), 400
            flash('Username and password are required.', 'danger')
            return render_template('auth/login.html')

        success, result = AuthService.login(
            username=username,
            password=password,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
        )

        if not success:
            if request.is_json:
                return jsonify({'success': False, 'message': result}), 401
            flash(result, 'danger')
            return render_template('auth/login.html', username=username)

        # API response with tokens in JSON
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'data': result,
            }), 200

        # Web: set cookies and redirect
        response = make_response(redirect(url_for('dashboard.index')))
        set_access_cookies(response, result['access_token'])
        set_refresh_cookies(response, result['refresh_token'])
        flash(f"Welcome back, {result['user']['first_name']}!", 'success')
        return response

    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logout — blacklists JWT and clears cookies."""
    try:
        verify_jwt_in_request(optional=True)
        jwt_data = get_jwt()
        if jwt_data:
            jti = jwt_data.get('jti')
            user_id = get_jwt_identity()
            exp = datetime.fromtimestamp(jwt_data['exp'], tz=timezone.utc).replace(tzinfo=None)
            AuthService.logout(jti=jti, user_id=user_id, expires_at=exp)
    except Exception:
        pass

    if request.is_json:
        return jsonify({'success': True, 'message': 'Logged out successfully'})

    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response)
    flash('You have been logged out successfully.', 'info')
    return response


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Issue a new access token using a valid refresh token."""
    try:
        verify_jwt_in_request(refresh=True)
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=str(user_id))

        if request.is_json:
            return jsonify({'success': True, 'access_token': new_token})

        response = make_response(jsonify({'success': True}))
        set_access_cookies(response, new_token)
        return response

    except Exception as e:
        return jsonify({'success': False, 'message': 'Invalid or expired refresh token'}), 401


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password reset request page."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        # TODO: implement email reset token logic
        flash('If that email is registered, a reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html')
