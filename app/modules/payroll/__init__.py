"""Payroll integration module reserved for future expansion."""
SLUG = 'payroll'
NAME = 'Payroll Integration'
FEATURES = ('Payroll Attendance Summary', 'Present Days', 'Absent Days', 'Paid Leave', 'Unpaid Leave', 'Overtime Calculation', 'Working Hours Summary', 'Payroll Export', 'Payroll Integration Settings')
SIDEBAR = ()

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
