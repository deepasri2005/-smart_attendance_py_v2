"""
Attendance, AttendanceLog, AttendanceRegularization, FaceProfile,
FaceEncoding, CCTVCamera, CCTVDetectionLog Models
"""
from datetime import datetime
from app.extensions import db


class Attendance(db.Model):
    """Main attendance record table."""
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    working_minutes = db.Column(db.Integer, default=0)

    attendance_status = db.Column(db.String(50), default='PRESENT')
    check_in_method = db.Column(db.String(50), nullable=True)
    check_out_method = db.Column(db.String(50), nullable=True)

    check_in_latitude = db.Column(db.Numeric(10, 8), nullable=True)
    check_in_longitude = db.Column(db.Numeric(11, 8), nullable=True)
    check_out_latitude = db.Column(db.Numeric(10, 8), nullable=True)
    check_out_longitude = db.Column(db.Numeric(11, 8), nullable=True)

    check_in_image = db.Column(db.String(500), nullable=True)
    check_out_image = db.Column(db.String(500), nullable=True)
    confidence_score = db.Column(db.Float, nullable=True)

    is_late = db.Column(db.Boolean, default=False)
    late_minutes = db.Column(db.Integer, default=0)
    early_departure_minutes = db.Column(db.Integer, default=0)
    overtime_minutes = db.Column(db.Integer, default=0)

    device_id = db.Column(db.String(255))

    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    remarks = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def attendance_method(self):
        return self.check_in_method or self.check_out_method

    user = db.relationship('User', foreign_keys=[user_id])
    approver = db.relationship('User', foreign_keys=[approved_by])
    logs = db.relationship('AttendanceLog', backref='attendance', lazy='dynamic')

    @property
    def employee_id(self):
        return self.user_id

    STATUS_PRESENT = 'PRESENT'
    STATUS_ABSENT = 'ABSENT'
    STATUS_HALF_DAY = 'HALF_DAY'
    STATUS_LATE = 'LATE'
    STATUS_ON_LEAVE = 'ON_LEAVE'
    STATUS_WFH = 'WFH'
    STATUS_ON_TOUR = 'ON_TOUR'
    STATUS_HOLIDAY = 'HOLIDAY'
    STATUS_WEEK_OFF = 'WEEK_OFF'

    METHOD_FACE = 'FACE'
    METHOD_CCTV = 'CCTV'
    METHOD_GEO = 'GEO'
    METHOD_MANUAL = 'MANUAL'

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'user_id': self.user_id,
            'employee_id': self.user_id,
            'attendance_date': self.attendance_date.isoformat() if self.attendance_date else None,
            'check_in': str(self.check_in) if self.check_in else None,
            'check_out': str(self.check_out) if self.check_out else None,
            'working_minutes': self.working_minutes,
            'attendance_status': self.attendance_status,
            'attendance_method': self.attendance_method,
            'is_late': self.is_late,
            'late_minutes': self.late_minutes,
            'overtime_minutes': self.overtime_minutes,
            'confidence_score': self.confidence_score,
        }


class AttendanceLog(db.Model):
    """Immutable audit trail for every attendance change."""
    __tablename__ = 'attendance_logs'

    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    action = db.Column('action_type', db.String(50))
    changed_by = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=True)
    action_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AttendanceRegularization(db.Model):
    """Employee requests to correct attendance."""
    __tablename__ = 'attendance_regularization'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'), nullable=True)
    attendance_date = db.Column(db.Date, nullable=False)
    request_type = db.Column(db.String(30))
    requested_check_in = db.Column(db.Time, nullable=True)
    requested_check_out = db.Column(db.Time, nullable=True)
    reason = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(255))
    status = db.Column(db.String(20), default='PENDING')
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    remarks = db.Column('approver_remarks', db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id])
    approver = db.relationship('User', foreign_keys=[approved_by])

    @property
    def employee_id(self):
        return self.user_id

    def to_dict(self):
        return {
            'id': self.id,
            'attendance_date': self.attendance_date.isoformat() if self.attendance_date else None,
            'request_type': self.request_type,
            'requested_check_in': str(self.requested_check_in) if self.requested_check_in else None,
            'requested_check_out': str(self.requested_check_out) if self.requested_check_out else None,
            'reason': self.reason,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class FaceProfile(db.Model):
    """Employee face recognition profile."""
    __tablename__ = 'face_profiles'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    registered_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    encodings = db.relationship('FaceEncoding', backref='face_profile', lazy='dynamic')
    user = db.relationship('User', foreign_keys=[user_id])

    @property
    def employee_id(self):
        return self.user_id


class FaceEncoding(db.Model):
    """Stored face encodings (binary blobs) per employee."""
    __tablename__ = 'face_encodings'

    id = db.Column(db.Integer, primary_key=True)
    face_profile_id = db.Column(db.Integer, db.ForeignKey('face_profiles.id'), nullable=False)
    encoding_data = db.Column('face_encoding', db.LargeBinary, nullable=False)
    image_path = db.Column(db.String(255))
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CCTVCamera(db.Model):
    """CCTV camera registry."""
    __tablename__ = 'cctv_cameras'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('organization_locations.id'), nullable=True)
    name = db.Column('camera_name', db.String(200), nullable=False)
    camera_code = db.Column('camera_code', db.String(100))
    rtsp_url = db.Column(db.Text)
    username = db.Column('camera_username', db.String(100))
    password_enc = db.Column('camera_password_encrypted', db.String(255))
    status = db.Column('camera_status', db.String(20), default='OFFLINE')
    is_active = db.Column(db.Boolean, default=True)
    last_heartbeat = db.Column('last_seen_at', db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    detection_logs = db.relationship('CCTVDetectionLog', backref='camera', lazy='dynamic')

    @property
    def camera_location(self):
        return self.camera_code or 'Main Entrance'

    def to_dict(self, include_rtsp=False):
        data = {
            'id': self.id,
            'name': self.name,
            'camera_location': self.camera_location,
            'status': self.status,
            'is_active': self.is_active,
            'last_heartbeat': self.last_heartbeat.isoformat() if self.last_heartbeat else None,
        }
        if include_rtsp:
            data['rtsp_url'] = self.rtsp_url
        return data


class CCTVDetectionLog(db.Model):
    """Log of every face detection event from CCTV."""
    __tablename__ = 'cctv_detection_logs'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    camera_id = db.Column(db.Integer, db.ForeignKey('cctv_cameras.id'), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=True)
    confidence_score = db.Column(db.Float)
    detected_at = db.Column('detection_time', db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(255))
    attendance_marked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id])


class AttendanceAnomaly(db.Model):
    """AI-detected attendance anomalies."""
    __tablename__ = 'attendance_anomalies'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'), nullable=True)
    anomaly_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    severity = db.Column(db.String(20), default='LOW')
    is_resolved = db.Column('status', db.Boolean, default=False)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column('detected_at', db.DateTime, default=datetime.utcnow)
