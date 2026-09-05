"""Attendance management module."""
SLUG = 'attendance'
NAME = 'Attendance Management'
FEATURES = ('Attendance Dashboard', 'Face Attendance', 'CCTV Attendance', 'Geo Attendance', 'Manual Attendance', 'QR Attendance', 'Check-In', 'Check-Out', 'Attendance Logs', 'Attendance History', 'Attendance Regularization', 'Attendance Approval', 'Missing Attendance', 'Late Attendance', 'Early Departure', 'Half-Day Attendance', 'Overtime Management', 'Attendance Anomalies')
SIDEBAR = ('Attendance Dashboard', 'Face Attendance', 'CCTV Attendance', 'Geo Attendance', 'Manual Attendance', 'Attendance History', 'Attendance Regularization', 'Attendance Approval', 'Attendance Anomalies')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
