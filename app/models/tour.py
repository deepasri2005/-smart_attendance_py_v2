"""
Tour (Official Duty) Application Model
"""
from datetime import datetime
from app.extensions import db


class TourApplication(db.Model):
    """Employee tour / official duty requests."""
    __tablename__ = 'tour_applications'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee_profiles.id'), nullable=False)
    tour_location = db.Column(db.String(300), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    estimated_expenses = db.Column(db.Numeric(10, 2), default=0)
    travel_mode = db.Column(db.String(50))  # AIR, TRAIN, BUS, CAR, OTHER
    travel_details = db.Column(db.Text)
    attachment = db.Column(db.String(255))
    status = db.Column(db.String(20), default='PENDING')
    # PENDING, APPROVED, REJECTED, CANCELLED, COMPLETED
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    remarks = db.Column(db.Text)

    # Expense settlement
    actual_expenses = db.Column(db.Numeric(10, 2), default=0)
    expense_bill = db.Column(db.String(255))
    expense_status = db.Column(db.String(20))  # PENDING, SUBMITTED, APPROVED, REJECTED

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = db.relationship('EmployeeProfile', backref='tour_applications')
    approver = db.relationship('User', foreign_keys=[approved_by])

    __table_args__ = (
        db.Index('idx_tour_org', 'organization_id'),
        db.Index('idx_tour_emp', 'employee_id'),
        db.Index('idx_tour_status', 'status'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'tour_location': self.tour_location,
            'from_date': self.from_date.isoformat() if self.from_date else None,
            'to_date': self.to_date.isoformat() if self.to_date else None,
            'total_days': self.total_days,
            'purpose': self.purpose,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
