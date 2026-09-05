"""
User, LoginDetails, LoginHistory, RefreshToken, DeviceRegistration Models
"""
from datetime import datetime
from app.extensions import db, bcrypt


class User(db.Model):
    """Core user entity — linked to organization."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column('mobile_number', db.String(20))
    profile_image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    login_details = db.relationship('LoginDetails', backref='user', uselist=False)
    employee_profile = db.relationship('EmployeeProfile', backref='user', uselist=False, foreign_keys='EmployeeProfile.user_id')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    permissions = db.relationship('UserPermission', backref='user', lazy='dynamic')

    @property
    def role_id(self):
        return self.login_details.role_id if self.login_details else None

    @property
    def role(self):
        if self.login_details and self.login_details.role_id:
            from app.models.role import Role
            return db.session.get(Role, self.login_details.role_id)
        return None

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def role_name(self):
        r = self.role
        return r.name if r else None

    @property
    def role_display_name(self):
        if self.is_super_admin:
            return 'Super Admin'
        elif self.is_org_admin:
            return 'Org Admin'
        elif self.is_emp_admin:
            return 'Emp Admin'
        elif self.is_employee:
            return 'Employee'
        return self.role_name or 'User'

    @property
    def is_super_admin(self):
        name = (self.role_name or '').upper()
        slug = (self.role.slug if self.role else '').lower()
        return name in ('SUPER_ADMIN', 'SUPER ADMIN', 'ADMIN') or slug in ('super_admin', 'admin')

    @property
    def is_org_admin(self):
        name = (self.role_name or '').upper()
        slug = (self.role.slug if self.role else '').lower()
        return name in ('ORG_ADMIN', 'ORGANIZATION ADMIN', 'ORG ADMIN', 'ORGADMIN') or slug in ('org_admin', 'orgadmin')

    @property
    def is_emp_admin(self):
        name = (self.role_name or '').upper()
        slug = (self.role.slug if self.role else '').lower()
        return name in ('EMP_ADMIN', 'EMPLOYEE ADMIN', 'EMP ADMIN', 'EMPADMIN', 'EMPLOYEE MANAGER') or slug in ('emp_admin', 'empadmin')

    @property
    def is_employee(self):
        name = (self.role_name or '').upper()
        slug = (self.role.slug if self.role else '').lower()
        return name in ('EMPLOYEE', 'EMP') or slug in ('employee', 'emp')

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'role': self.role_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'profile_image': self.profile_image,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<User {self.email}>'


class LoginDetails(db.Model):
    """Username/password credentials for a user."""
    __tablename__ = 'login_details'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150))
    mobile_number = db.Column(db.String(20))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    failed_attempts = db.Column('failed_login_attempts', db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    password_changed_at = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_ld_username', 'username'),
        db.Index('idx_ld_user', 'user_id'),
    )

    def set_password(self, password):
        """Hash and store a password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verify a password against the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_locked(self):
        """Check if account is currently locked."""
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False

    def __repr__(self):
        return f'<LoginDetails {self.username}>'


class RefreshToken(db.Model):
    """Stores refresh token hashes for revocation support."""
    __tablename__ = 'refresh_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    jti = db.Column(db.String(36), unique=True, nullable=False)  # JWT ID claim
    token_hash = db.Column(db.String(255))
    device_info = db.Column(db.String(255))
    ip_address = db.Column(db.String(50))
    expires_at = db.Column(db.DateTime, nullable=False)
    is_revoked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_rt_user', 'user_id'),
        db.Index('idx_rt_jti', 'jti'),
    )

    def __repr__(self):
        return f'<RefreshToken user={self.user_id}>'


class TokenBlocklist(db.Model):
    """JWT token blacklist for logout / revocation."""
    __tablename__ = 'token_blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    token_type = db.Column(db.String(10))  # access / refresh
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        db.Index('idx_tb_jti', 'jti'),
    )


class LoginHistory(db.Model):
    """Tracks every login attempt (success or failure)."""
    __tablename__ = 'login_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    username_attempted = db.Column('username', db.String(100))
    status = db.Column('login_status', db.String(20))
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.Text)
    created_at = db.Column('login_at', db.DateTime, default=datetime.utcnow)


class DeviceRegistration(db.Model):
    """Trusted devices registered by users."""
    __tablename__ = 'device_registrations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    device_id = db.Column(db.String(255), nullable=False)
    device_name = db.Column(db.String(100))
    browser = db.Column(db.String(100))
    os = db.Column(db.String(100))
    ip_address = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_dr_user', 'user_id'),
    )
