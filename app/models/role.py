"""
Role, Module, SubModule, and Permission Models
Dynamic RBAC system.
"""
from datetime import datetime
from app.extensions import db


class Role(db.Model):
    """User roles (SUPER_ADMIN, ORG_ADMIN, EMP_ADMIN, EMPLOYEE)."""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('role_name', db.String(50), nullable=False)
    slug = db.Column('role_slug', db.String(50))
    description = db.Column(db.Text)
    is_system_role = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def display_name(self):
        return self.name

    SUPER_ADMIN = 'Super Admin'
    ORG_ADMIN = 'Org Admin'
    EMP_ADMIN = 'Emp Admin'
    EMPLOYEE = 'Employee'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.name,
            'description': self.description,
            'is_system_role': self.is_system_role,
        }

    def __repr__(self):
        return f'<Role {self.name}>'


class Module(db.Model):
    """Application modules (Dashboard, Attendance, Leave, etc.)."""
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('module_name', db.String(100), nullable=False)
    slug = db.Column('module_slug', db.String(100), unique=True, nullable=False)
    icon = db.Column('module_icon', db.String(50), default='bi-circle')
    route = db.Column('route_name', db.String(200))
    order = db.Column('display_order', db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sub_modules = db.relationship('SubModule', backref='module', lazy='dynamic', order_by='SubModule.order')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'icon': self.icon,
            'route': self.route,
            'order': self.order,
        }

    def __repr__(self):
        return f'<Module {self.name}>'


class SubModule(db.Model):
    """Sub-modules within a module (Face Attendance, Geo Attendance, etc.)."""
    __tablename__ = 'sub_modules'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    name = db.Column('sub_module_name', db.String(100), nullable=False)
    slug = db.Column('sub_module_slug', db.String(100), nullable=False)
    route = db.Column('route_name', db.String(200))
    order = db.Column('display_order', db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def icon(self):
        return 'bi-dot'

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'name': self.name,
            'slug': self.slug,
            'icon': self.icon,
            'route': self.route,
        }

    def __repr__(self):
        return f'<SubModule {self.name}>'


class Permission(db.Model):
    """Permission types (view, create, edit, delete, approve, etc.)."""
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('permission_slug', db.String(50), unique=True, nullable=False)
    display_name = db.Column('permission_name', db.String(100))

    VIEW = 'view'
    CREATE = 'create'
    EDIT = 'edit'
    DELETE = 'delete'
    APPROVE = 'approve'
    REJECT = 'reject'
    EXPORT = 'export'
    MANAGE = 'manage'

    def __repr__(self):
        return f'<Permission {self.name}>'


class RolePermission(db.Model):
    """Maps roles to module/sub-module permissions."""
    __tablename__ = 'role_permissions'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    sub_module_id = db.Column(db.Integer, db.ForeignKey('sub_modules.id'), nullable=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.relationship('Role', backref='role_permissions')
    module = db.relationship('Module')
    sub_module = db.relationship('SubModule')
    permission = db.relationship('Permission')

    __table_args__ = (
        db.Index('idx_rp_role', 'role_id'),
        db.Index('idx_rp_module', 'module_id'),
        db.UniqueConstraint('role_id', 'module_id', 'sub_module_id', 'permission_id', name='uq_role_perm'),
    )


class UserPermission(db.Model):
    """Individual user permission overrides."""
    __tablename__ = 'user_permissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    sub_module_id = db.Column(db.Integer, db.ForeignKey('sub_modules.id'), nullable=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    is_granted = db.Column(db.Boolean, default=True)  # False = explicit deny
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_up_user', 'user_id'),
    )
