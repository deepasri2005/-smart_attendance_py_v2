"""
Organization Model
"""
from datetime import datetime
from app.extensions import db


class Organization(db.Model):
    """Multi-tenant organization table."""
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('organization_name', db.String(200), nullable=False)
    slug = db.Column('organization_code', db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150))
    phone = db.Column('mobile_number', db.String(20))
    address = db.Column(db.Text)
    logo = db.Column(db.String(255))
    website = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100), default='India')
    postal_code = db.Column('pincode', db.String(20))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = db.relationship('User', backref='organization', lazy='dynamic')
    departments = db.relationship('Department', backref='organization', lazy='dynamic')
    locations = db.relationship('OrganizationLocation', backref='organization', lazy='dynamic')
    shifts = db.relationship('Shift', backref='organization', lazy='dynamic')
    attendance_rules = db.relationship('AttendanceRule', backref='organization', uselist=False)

    @property
    def gstin(self):
        return None

    @property
    def timezone(self):
        return 'Asia/Kolkata'

    __table_args__ = (
        db.Index('idx_org_slug', 'organization_code'),
        db.Index('idx_org_active', 'is_active'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'logo': self.logo,
            'website': self.website,
            'timezone': self.timezone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Organization {self.name}>'
