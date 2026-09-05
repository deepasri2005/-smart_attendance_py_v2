"""
Notification Model
"""
from datetime import datetime
from app.extensions import db


class Notification(db.Model):
    """In-app notifications for users."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(30), default='INFO')
    # INFO, SUCCESS, WARNING, DANGER, LEAVE, TOUR, WFH, ATTENDANCE, SYSTEM

    reference_type = db.Column(db.String(50))   # leave_application, tour_application, etc.
    reference_id = db.Column(db.Integer)

    @property
    def icon(self):
        return 'bi-bell'

    @property
    def link(self):
        return '#'

    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_notif_user', 'user_id'),
        db.Index('idx_notif_org', 'organization_id'),
        db.Index('idx_notif_created', 'created_at'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'reference_type': self.reference_type,
            'reference_id': self.reference_id,
            'icon': self.icon,
            'link': self.link,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
