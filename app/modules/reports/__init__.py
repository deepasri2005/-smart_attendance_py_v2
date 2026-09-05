"""Reports and analytics module."""
SLUG = 'reports'
NAME = 'Reports & Analytics'
FEATURES = ('Attendance Reports', 'Daily Attendance Report', 'Monthly Attendance Report', 'Employee-Wise Report', 'Department-Wise Report', 'Organization-Wise Report', 'Face Attendance Report', 'CCTV Attendance Report', 'Geo Attendance Report', 'Late Attendance Report', 'Absent Report', 'Overtime Report', 'Leave Reports', 'Tour Reports', 'WFH Reports', 'Employee Reports', 'Custom Reports', 'Export Excel', 'Export CSV', 'Export PDF', 'Analytics Dashboard')
SIDEBAR = ('Attendance Reports', 'Employee Reports', 'Leave Reports', 'Tour Reports', 'WFH Reports', 'Analytics Dashboard')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
