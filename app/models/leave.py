"""
Leave Management Models: LeaveType, LeaveBalance, LeaveApplication
"""
from datetime import datetime
from app.extensions import db


class LeaveType(db.Model):
    """Types of leaves (Casual, Sick, Earned, etc.)."""
    __tablename__ = 'leave_types'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column('leave_name', db.String(100), nullable=False)
    code = db.Column('leave_code', db.String(20), nullable=False)  # CL, SL, EL, etc.
    days_allowed_per_year = db.Column('total_days_per_year', db.Integer, default=0)
    is_paid = db.Column(db.Boolean, default=True)
    requires_document = db.Column(db.Boolean, default=False)
    allow_half_day = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    balances = db.relationship('LeaveBalance', backref='leave_type', lazy='dynamic')
    applications = db.relationship('LeaveApplication', backref='leave_type', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'days_allowed_per_year': self.days_allowed_per_year,
            'is_paid': self.is_paid,
            'carry_forward': self.carry_forward,
            'color': self.color,
        }


class LeaveBalance(db.Model):
    """Annual leave balance per employee per leave type."""
    __tablename__ = 'leave_balances'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_types.id'), nullable=False)
    year = db.Column('leave_year', db.Integer, nullable=False)
    total_days = db.Column('allocated_days', db.Float, default=0)
    used_days = db.Column(db.Float, default=0)
    pending_days = db.Column(db.Float, default=0)
    carried_forward = db.Column(db.Float, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def employee_id(self):
        return self.user_id

    __table_args__ = (
        db.UniqueConstraint('user_id', 'leave_type_id', 'leave_year', name='uq_leave_balance'),
        db.Index('idx_lb_emp', 'user_id'),
        db.Index('idx_lb_org', 'organization_id'),
    )

    @property
    def available_days(self):
        return self.total_days - self.used_days - self.pending_days

    def to_dict(self):
        return {
            'id': self.id,
            'leave_type_id': self.leave_type_id,
            'leave_type': self.leave_type.name if self.leave_type else None,
            'year': self.year,
            'total_days': self.total_days,
            'used_days': self.used_days,
            'pending_days': self.pending_days,
            'available_days': self.available_days,
        }


class LeaveApplication(db.Model):
    """Employee leave applications."""
    __tablename__ = 'leave_applications'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_types.id'), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Float, nullable=False)
    is_half_day = db.Column(db.Boolean, default=False)
    half_day_period = db.Column('half_day_type', db.String(50))
    reason = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(255))
    status = db.Column(db.String(20), default='PENDING')
    # PENDING, APPROVED, REJECTED, CANCELLED
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

    __table_args__ = (
        db.Index('idx_la_org', 'organization_id'),
        db.Index('idx_la_emp', 'user_id'),
        db.Index('idx_la_status', 'status'),
        db.Index('idx_la_dates', 'from_date', 'to_date'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'leave_type_id': self.leave_type_id,
            'leave_type': self.leave_type.name if self.leave_type else None,
            'from_date': self.from_date.isoformat() if self.from_date else None,
            'to_date': self.to_date.isoformat() if self.to_date else None,
            'total_days': self.total_days,
            'reason': self.reason,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
