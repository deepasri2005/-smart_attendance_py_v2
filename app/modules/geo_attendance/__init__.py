"""Geo attendance management module."""
SLUG = 'geo-attendance'
NAME = 'Geo Attendance Management'
FEATURES = ('Geo Attendance', 'Organization Locations', 'Geo-Fence Management', 'Allowed Radius Settings', 'Employee Location Tracking', 'Location History', 'Check-In Location', 'Check-Out Location', 'Geo Attendance Logs', 'Geo Attendance Settings', 'Location Exception Requests')
SIDEBAR = ('Geo Attendance', 'Geo-Fence Management', 'Employee Location Tracking', 'Location History', 'Geo Attendance Logs')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
