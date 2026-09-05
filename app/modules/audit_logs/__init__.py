"""Audit and system logs module."""
SLUG = 'audit-logs'
NAME = 'Audit & System Logs'
FEATURES = ('Audit Logs', 'User Activity Logs', 'Login Logs', 'Attendance Change Logs', 'Approval Logs', 'API Logs', 'Error Logs', 'System Activity Logs')
SIDEBAR = ()

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
