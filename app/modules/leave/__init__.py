"""Leave management module."""
SLUG = 'leave'
NAME = 'Leave Management'
FEATURES = ('Leave Dashboard', 'Leave Types', 'Leave Policies', 'Leave Balance', 'Apply Leave', 'My Leave Applications', 'Leave Approval', 'Leave Rejection', 'Leave Cancellation', 'Half-Day Leave', 'Leave History', 'Leave Calendar', 'Leave Reports')
SIDEBAR = ('Apply Leave', 'My Leave Applications', 'Leave Approval', 'Leave Balance', 'Leave Types', 'Leave Reports')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
