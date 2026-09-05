"""Synchronize the module catalog and default role permissions."""
from app.extensions import db
from app.modules import MODULES, permission_actions
from app.models.role import Module, SubModule, Permission, Role, RolePermission

MODULE_ALIASES = {
    'organization': 'organization_management',
    'employees': 'employee_management',
    'work-from-home': 'work_from_home',
    'audit-logs': 'audit_logs',
}

MODULE_ICONS = {
    'dashboard': 'bi-speedometer2',
    'organization': 'bi-buildings',
    'users-access': 'bi-shield-lock',
    'employees': 'bi-people-fill',
    'attendance': 'bi-clock-fill',
    'face-ai': 'bi-person-bounding-box',
    'cctv': 'bi-camera-video-fill',
    'geo-attendance': 'bi-geo-alt-fill',
    'shifts': 'bi-calendar-week',
    'leave': 'bi-calendar-minus',
    'tour': 'bi-map',
    'work-from-home': 'bi-house',
    'approvals': 'bi-check2-square',
    'notifications': 'bi-bell',
    'reports': 'bi-bar-chart',
    'payroll': 'bi-wallet2',
    'ai-anomalies': 'bi-robot',
    'security': 'bi-shield-check',
    'audit-logs': 'bi-journal-text',
    'settings': 'bi-gear',
}

ROLE_MODULES = {
    'SUPER_ADMIN': set(MODULES),
    'ORG_ADMIN': {
        'dashboard', 'organization', 'users-access', 'employees', 'attendance', 'face-ai', 'cctv',
        'geo-attendance', 'shifts', 'leave', 'tour', 'work-from-home',
        'approvals', 'notifications', 'reports', 'settings',
    },
    'EMP_ADMIN': {
        'dashboard', 'employees', 'attendance', 'face-ai', 'cctv',
        'geo-attendance', 'leave', 'tour', 'work-from-home', 'approvals', 'reports', 'settings',
    },
    'EMPLOYEE': {
        'dashboard', 'attendance', 'leave', 'tour', 'work-from-home', 'notifications', 'settings',
    },
}

ROLE_ACTIONS = {
    'SUPER_ADMIN': set(permission_actions()),
    'ORG_ADMIN': set(permission_actions()),
    'EMP_ADMIN': {'view', 'create', 'edit', 'approve', 'reject', 'export'},
    'EMPLOYEE': {'view', 'create', 'edit'},
}

ROLE_FORBIDDEN_FEATURES = {
    'ORG_ADMIN': {
        'settings': {'security-settings', 'role-&-permission-settings', 'jwt-settings', 'backup-settings', 'email-settings', 'sms-settings', 'whatsapp-settings'},
    },
    'EMP_ADMIN': {
        'settings': {'general-settings', 'company-settings', 'attendance-settings', 'face-recognition-settings', 'cctv-settings', 'geo-attendance-settings', 'leave-settings', 'email-settings', 'sms-settings', 'whatsapp-settings', 'jwt-settings', 'security-settings', 'backup-settings', 'role-&-permission-settings'},
    },
    'EMPLOYEE': {
        'settings': {'general-settings', 'company-settings', 'attendance-settings', 'face-recognition-settings', 'cctv-settings', 'geo-attendance-settings', 'leave-settings', 'notification-settings', 'email-settings', 'sms-settings', 'whatsapp-settings', 'jwt-settings', 'security-settings', 'backup-settings', 'role-&-permission-settings'},
    },
}


def _slug(value):
    return value.lower().replace(' / ', '-').replace(' & ', '-').replace(' ', '-').replace('/', '-')


def _find_role(role_slug, role_name):
    role = Role.query.filter_by(slug=role_slug).first()
    if not role:
        role = Role.query.filter_by(name=role_name).first()
    if not role:
        role = Role(name=role_name, slug=role_slug, is_system_role=True, is_active=True)
        db.session.add(role)
        db.session.flush()
    else:
        role.name = role_name
        db.session.flush()
    return role


def _find_or_create_permission(name):
    permission = Permission.query.filter_by(name=name).first()
    if not permission:
        permission = Permission(name=name, display_name=name.replace('_', ' ').title())
        db.session.add(permission)
        db.session.flush()
    return permission


def sync_module_catalog():
    """Upsert catalog records and default role permissions in the current database."""
    permissions = {name: _find_or_create_permission(name) for name in permission_actions()}
    module_records = {}

    for order, definition in enumerate(MODULES.values(), start=1):
        slug = definition['slug']
        module = Module.query.filter_by(slug=slug).first()
        if not module:
            legacy_slug = MODULE_ALIASES.get(slug)
            module = Module.query.filter_by(slug=legacy_slug).first() if legacy_slug else None
        if not module:
            module = Module(slug=slug)
            db.session.add(module)

        module.name = definition['name']
        module.slug = slug
        module.icon = MODULE_ICONS.get(slug, 'bi-grid')
        module.route = '/dashboard/' if slug == 'dashboard' else f'/modules/{slug}'
        module.order = order
        module.is_active = True
        db.session.flush()
        module_records[slug] = module

        for feature_order, feature in enumerate(definition['features'], start=1):
            feature_slug = feature['slug']
            sub_module = SubModule.query.filter_by(
                module_id=module.id, slug=feature_slug
            ).first()
            if not sub_module:
                sub_module = SubModule.query.filter_by(
                    module_id=module.id, name=feature['name']
                ).first()
            if not sub_module:
                sub_module = SubModule(module_id=module.id, slug=feature_slug)
                db.session.add(sub_module)
            sub_module.name = feature['name']
            sub_module.slug = feature_slug
            sub_module.route = (
                '/dashboard/' if slug == 'dashboard' else
                f'/modules/{slug}/{feature_slug}'
            )
            sub_module.order = feature_order
            sub_module.is_active = True

    db.session.flush()

    role_specs = {
        'SUPER_ADMIN': ('Super Admin', 'super_admin'),
        'ORG_ADMIN': ('Org Admin', 'org_admin'),
        'EMP_ADMIN': ('Emp Admin', 'emp_admin'),
        'EMPLOYEE': ('Employee', 'emp'),
    }
    for role_code, (role_name, role_slug) in role_specs.items():
        role = _find_role(role_slug, role_name)
        allowed_modules = ROLE_MODULES[role_code]
        allowed_actions = ROLE_ACTIONS[role_code]
        forbidden_features = ROLE_FORBIDDEN_FEATURES.get(role_code, {})

        # 1. Purge permissions for modules not in allowed_modules
        allowed_module_ids = {module_records[slug].id for slug in allowed_modules if slug in module_records}
        RolePermission.query.filter(
            RolePermission.role_id == role.id,
            ~RolePermission.module_id.in_(allowed_module_ids)
        ).delete(synchronize_session=False)

        # 2. Grant or clean feature-level permissions within allowed modules
        for module_slug in allowed_modules:
            module = module_records[module_slug]
            forbidden_in_module = forbidden_features.get(module_slug, set())
            for feature in module.sub_modules.order_by(SubModule.order).all():
                if feature.slug in forbidden_in_module:
                    RolePermission.query.filter_by(
                        role_id=role.id,
                        module_id=module.id,
                        sub_module_id=feature.id,
                    ).delete(synchronize_session=False)
                    continue

                for action in allowed_actions:
                    permission = permissions[action]
                    exists = RolePermission.query.filter_by(
                        role_id=role.id,
                        module_id=module.id,
                        sub_module_id=feature.id,
                        permission_id=permission.id,
                    ).first()
                    if not exists:
                        db.session.add(RolePermission(
                            role_id=role.id,
                            module_id=module.id,
                            sub_module_id=feature.id,
                            permission_id=permission.id,
                        ))

    db.session.commit()
    return module_records
