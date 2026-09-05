"""
Flask Application Factory
"""
import os
import logging
from flask import Flask, render_template, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from config import config_by_name
from app.extensions import db, migrate, jwt, bcrypt, csrf, mail, limiter


def create_app(config_name: str = None) -> Flask:
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # ── Extensions ────────────────────────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    # ── Logging ───────────────────────────────────────────────────────────────
    if not app.debug:
        logging.basicConfig(level=logging.INFO)

    # ── JWT Callbacks ─────────────────────────────────────────────────────────
    _register_jwt_callbacks(app)

    # ── Blueprints ────────────────────────────────────────────────────────────
    _register_blueprints(app)

    # ── Error Handlers ────────────────────────────────────────────────────────
    _register_error_handlers(app)

    # ── Shell Context ─────────────────────────────────────────────────────────
    _register_shell_context(app)

    # ── Upload Folder ─────────────────────────────────────────────────────────
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app


def _register_jwt_callbacks(app: Flask):
    """Register JWT event callbacks."""
    from app.models.user import TokenBlocklist
    from flask_jwt_extended import get_jwt

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get('jti')
        try:
            return db.session.query(TokenBlocklist).filter_by(jti=jti).first() is not None
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Token has expired'}), 401
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Authentication required'}), 401
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))


def _register_blueprints(app: Flask):
    """Register all Flask Blueprints."""
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.attendance import attendance_bp
    from app.routes.cctv import cctv_bp
    from app.routes.modules import modules_bp
    from app.routes.module_pages import module_pages_bp
    from app.routes.organization import organization_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(cctv_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(module_pages_bp)
    app.register_blueprint(organization_bp)

    # Exempt API routes from CSRF
    csrf.exempt(auth_bp)
    csrf.exempt(attendance_bp)
    csrf.exempt(cctv_bp)
    csrf.exempt(modules_bp)
    csrf.exempt(organization_bp)


def _register_error_handlers(app: Flask):
    """Register custom error pages."""
    @app.errorhandler(403)
    def forbidden(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Forbidden', 'error': str(e)}), 403
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Not found'}), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Too many requests. Please slow down.'}), 429
        from flask import flash, redirect, url_for
        flash('Too many requests. Please wait a moment.', 'warning')
        return redirect(url_for('auth.login'))


def _register_shell_context(app: Flask):
    """Push models and db into the Flask shell context."""
    @app.shell_context_processor
    def make_shell_context():
        from app import models
        return {
            'db': db,
            **{name: getattr(models, name) for name in models.__all__}
        }
