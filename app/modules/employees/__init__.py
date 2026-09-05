"""Employee management module."""
SLUG = 'employees'
NAME = 'Employee Management'
FEATURES = ('Employee List', 'Add Employee', 'Edit Employee', 'Employee Profile', 'Employee Documents', 'Employee Department Assignment', 'Employee Designation Assignment', 'Reporting Manager', 'Employee Status', 'Employee Import', 'Employee Export', 'Employee Shift Assignment', 'Employee Face Registration')
SIDEBAR = ('Employee List', 'Add Employee', 'Employee Profile', 'Employee Face Registration', 'Employee Shift Assignment')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
