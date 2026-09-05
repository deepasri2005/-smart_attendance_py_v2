"""
Flask Extensions — instantiated here, initialized in app factory.
Import from here everywhere else to avoid circular imports.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
