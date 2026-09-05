"""User and access management module."""
SLUG = 'users-access'
NAME = 'User & Access Management'
FEATURES = ('Users', 'Login Details', 'Roles', 'Modules', 'Sub-Modules', 'Permissions', 'Role Permissions', 'User Permissions', 'User Activation / Deactivation', 'Password Reset', 'Login History', 'Device Management')
SIDEBAR = ('Users', 'Roles', 'Modules', 'Sub-Modules', 'Permissions', 'Role Permissions', 'User Permissions')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' / ', '-').replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
