"""Shift and work schedule management module."""
SLUG = 'shifts'
NAME = 'Shift & Work Schedule Management'
FEATURES = ('Shift List', 'Add Shift', 'Shift Settings', 'Shift Timing', 'Grace Period', 'Working Hours Rules', 'Half-Day Rules', 'Night Shift Management', 'Flexible Shift', 'Employee Shift Assignment', 'Shift Rotation', 'Work Calendar')
SIDEBAR = ('Shift List', 'Shift Settings', 'Employee Shift Assignment', 'Work Calendar')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
