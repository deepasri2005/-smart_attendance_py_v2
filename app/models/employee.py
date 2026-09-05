"""
Employee-related Models: Department, Designation, EmployeeProfile,
Shift, EmployeeShift, OrganizationLocation, AttendanceRule
"""
from datetime import datetime
from app.extensions import db


class Department(db.Model):
    """Organizational departments."""
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column('department_name', db.String(150), nullable=False)
    code = db.Column('department_code', db.String(20))
    description = db.Column(db.Text)
    head_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    head = db.relationship('User', foreign_keys=[head_user_id])
    employees = db.relationship('EmployeeProfile', backref='department', lazy='dynamic')
    designations = db.relationship('Designation', backref='department', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'name': self.name,
            'code': self.code,
            'is_active': self.is_active,
        }


class Designation(db.Model):
    """Employee designations/job titles."""
    __tablename__ = 'designations'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    name = db.Column('designation_name', db.String(150), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employees = db.relationship('EmployeeProfile', backref='designation', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class EmployeeProfile(db.Model):
    """Extended employee information linked to a User."""
    __tablename__ = 'employee_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    emp_code = db.Column(db.String(50), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    designation_id = db.Column(db.Integer, db.ForeignKey('designations.id'), nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    join_date = db.Column(db.Date, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(20))
    bank_account = db.Column(db.String(50))
    pan_number = db.Column(db.String(20))
    aadhar_number = db.Column(db.String(20))
    profile_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    manager = db.relationship('User', foreign_keys=[manager_id])

    @property
    def face_profile(self):
        from app.models.attendance import FaceProfile
        return FaceProfile.query.filter_by(user_id=self.user_id).first()

    __table_args__ = (
        db.Index('idx_emp_org', 'organization_id'),
        db.Index('idx_emp_dept', 'department_id'),
        db.UniqueConstraint('organization_id', 'emp_code', name='uq_emp_code'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'emp_code': self.emp_code,
            'department_id': self.department_id,
            'designation_id': self.designation_id,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'gender': self.gender,
            'full_name': self.user.full_name if self.user else None,
            'email': self.user.email if self.user else None,
        }


class Shift(db.Model):
    """Work shift definitions."""
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column('shift_name', db.String(100), nullable=False)
    code = db.Column('shift_code', db.String(50))
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    grace_minutes = db.Column(db.Integer, default=15)
    minimum_working_hours = db.Column('minimum_working_minutes', db.Float, default=480.0)
    half_day_hours = db.Column('half_day_minutes', db.Float, default=240.0)
    is_overnight = db.Column('is_night_shift', db.Boolean, default=False)
    is_flexible = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_shift_org', 'organization_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'grace_minutes': self.grace_minutes,
            'minimum_working_hours': self.minimum_working_hours,
        }


class EmployeeShift(db.Model):
    """Assignment of shifts to employees."""
    __tablename__ = 'employee_shifts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    effective_to = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shift = db.relationship('Shift')

    @property
    def employee_id(self):
        return self.user_id

    __table_args__ = (
        db.Index('idx_empshift_emp', 'user_id'),
    )


class OrganizationLocation(db.Model):
    """Office locations for geo-fence validation."""
    __tablename__ = 'organization_locations'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    location_name = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    allowed_radius_meters = db.Column(db.Integer, default=100)
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_loc_org', 'organization_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'location_name': self.location_name,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'allowed_radius_meters': self.allowed_radius_meters,
            'is_active': self.is_active,
        }


class AttendanceRule(db.Model):
    """Configurable attendance rules per organization."""
    __tablename__ = 'attendance_rules'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False, unique=True)
    minimum_working_hours = db.Column(db.Float, default=8.0)
    half_day_hours = db.Column(db.Float, default=4.0)
    late_grace_minutes = db.Column(db.Integer, default=15)
    early_departure_minutes = db.Column(db.Integer, default=15)
    cctv_cooldown_minutes = db.Column(db.Integer, default=30)
    face_cooldown_minutes = db.Column(db.Integer, default=10)
    geo_accuracy_limit_meters = db.Column(db.Integer, default=100)
    allowed_ips = db.Column(db.Text)  # Comma-separated IP list, null = any
    allow_manual_attendance = db.Column(db.Boolean, default=True)
    require_face_liveness = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Holiday(db.Model):
    """Holidays and week-off rules."""
    __tablename__ = 'holidays'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column('holiday_name', db.String(200), nullable=False)
    holiday_date = db.Column(db.Date, nullable=False)
    holiday_type = db.Column(db.String(20), default='ORG')  # NATIONAL, ORG, OPTIONAL
    description = db.Column(db.Text)
    is_optional = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_holiday_org', 'organization_id'),
        db.Index('idx_holiday_date', 'holiday_date'),
    )


class WeekOffRule(db.Model):
    """Weekly off day configuration per organization."""
    __tablename__ = 'week_off_rules'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    is_active = db.Column(db.Boolean, default=True)


