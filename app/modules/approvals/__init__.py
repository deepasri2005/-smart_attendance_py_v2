"""Centralized approval management module."""
SLUG = 'approvals'
NAME = 'Approval Management'
FEATURES = ('Pending Approvals', 'Attendance Approvals', 'Attendance Regularization Approval', 'Leave Approvals', 'Tour Approvals', 'WFH Approvals', 'Approval History', 'Rejected Requests', 'Approval Workflow Settings', 'Multi-Level Approval')
SIDEBAR = ('Pending Approvals', 'Attendance Approvals', 'Leave Approvals', 'Tour Approvals', 'WFH Approvals')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
