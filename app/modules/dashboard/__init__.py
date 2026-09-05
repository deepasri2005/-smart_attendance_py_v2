"""Dashboard module."""
SLUG = 'dashboard'
NAME = 'Dashboard'
FEATURES = ('Dashboard Overview', 'Attendance Summary', 'Employee Summary', 'Pending Approvals', 'Notifications Summary', 'Analytics & Charts')
SIDEBAR = FEATURES

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' & ', '-').replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
