"""
Application Configuration
All sensitive values are loaded from environment variables via .env
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    # Application
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/smart_attendance'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
    }

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_COOKIE_SECURE = False           # True in production (HTTPS)
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'

    # Session
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Redis / Celery
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'info@codevocado.in')

    # File Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    LOGIN_MAX_ATTEMPTS = 5
    LOGIN_LOCKOUT_MINUTES = 15

    # Timezone
    TIMEZONE = os.environ.get('TIMEZONE', 'Asia/Kolkata')

    # Face Recognition
    FACE_RECOGNITION_TOLERANCE = float(os.environ.get('FACE_RECOGNITION_TOLERANCE', '0.5'))
    FACE_DUPLICATE_COOLDOWN_MINUTES = int(os.environ.get('FACE_DUPLICATE_COOLDOWN_MINUTES', '10'))

    # CCTV
    CCTV_COOLDOWN_MINUTES = int(os.environ.get('CCTV_COOLDOWN_MINUTES', '30'))
    CCTV_FRAME_INTERVAL = int(os.environ.get('CCTV_FRAME_INTERVAL', '30'))  # seconds

    # Geo
    GEO_DEFAULT_RADIUS_METERS = int(os.environ.get('GEO_DEFAULT_RADIUS_METERS', '100'))

    # WTF / CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    RATELIMIT_ENABLED = False
    JWT_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False  # Easier dev experience; re-enable for staging


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    JWT_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ENGINE_OPTIONS = {}
    JWT_COOKIE_CSRF_PROTECT = False
    WTF_CSRF_ENABLED = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
