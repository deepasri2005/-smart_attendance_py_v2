"""
Audit Log Model — immutable system-wide activity log.
"""
from datetime import datetime
from app.extensions import db


class AuditLog(db.Model):
    """Immutable audit trail for all critical system actions."""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    # LOGIN, LOGOUT, FAILED_LOGIN, USER_CREATED, USER_UPDATED, ATTENDANCE_MARKED,
    # LEAVE_APPROVED, PERMISSION_CHANGED, etc.
    module = db.Column(db.String(100))
    record_type = db.Column(db.String(100))  # Table/model name
    record_id = db.Column(db.Integer)
    old_data = db.Column(db.JSON)
    new_data = db.Column(db.JSON)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'user_id': self.user_id,
            'action': self.action,
            'module': self.module,
            'record_type': self.record_type,
            'record_id': self.record_id,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
