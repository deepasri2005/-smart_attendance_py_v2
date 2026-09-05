"""Feature modules registry for the Smart Attendance application."""
from importlib import import_module

MODULE_PACKAGE_NAMES = (
    'dashboard', 'organization', 'users_access', 'employees', 'attendance',
    'face_ai', 'cctv', 'geo_attendance', 'shifts', 'leave', 'tour',
    'work_from_home', 'approvals', 'notifications', 'reports', 'payroll',
    'ai_anomalies', 'security', 'audit_logs', 'settings',
)


def _load_modules():
    return {
        definition['slug']: definition
        for package_name in MODULE_PACKAGE_NAMES
        for definition in [import_module(f'app.modules.{package_name}').get_definition()]
    }


MODULES = _load_modules()


def get_module(slug):
    """Return a module definition by slug, or None when it is unknown."""
    return MODULES.get(slug)


def sidebar_modules():
    """Return the recommended, compact sidebar representation."""
    return [
        {
            'slug': module['slug'],
            'name': module['name'],
            'features': [feature for feature in module['features'] if feature.get('sidebar')],
        }
        for module in MODULES.values()
    ]


def permission_actions():
    """Actions supported by every module and feature."""
    return ('view', 'create', 'edit', 'delete', 'approve', 'reject', 'export', 'manage')


__all__ = ['MODULES', 'get_module', 'permission_actions', 'sidebar_modules']
