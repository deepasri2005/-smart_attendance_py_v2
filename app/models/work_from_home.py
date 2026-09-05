"""
Work From Home Application Model
"""
from datetime import datetime
from app.extensions import db


class WFHApplication(db.Model):
    """Employee work-from-home requests."""
    __tablename__ = 'wfh_applications'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee_profiles.id'), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Float, nullable=False)
    is_half_day = db.Column(db.Boolean, default=False)
    half_day_period = db.Column(db.String(10))
    reason = db.Column(db.Text, nullable=False)
    work_location = db.Column(db.String(300))  # Home address / description
    status = db.Column(db.String(20), default='PENDING')
    # PENDING, APPROVED, REJECTED, CANCELLED
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    remarks = db.Column(db.Text)

    # Daily work report (optional advanced feature)
    task_report = db.Column(db.Text)
    check_in_time = db.Column(db.Time, nullable=True)
    check_out_time = db.Column(db.Time, nullable=True)
    check_in_latitude = db.Column(db.Numeric(10, 8), nullable=True)
    check_in_longitude = db.Column(db.Numeric(11, 8), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = db.relationship('EmployeeProfile', backref='wfh_applications')
    approver = db.relationship('User', foreign_keys=[approved_by])

    __table_args__ = (
        db.Index('idx_wfh_org', 'organization_id'),
        db.Index('idx_wfh_emp', 'employee_id'),
        db.Index('idx_wfh_status', 'status'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'from_date': self.from_date.isoformat() if self.from_date else None,
            'to_date': self.to_date.isoformat() if self.to_date else None,
            'total_days': self.total_days,
            'reason': self.reason,
            'work_location': self.work_location,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
