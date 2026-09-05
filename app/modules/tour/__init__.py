"""Tour and official duty management module."""
SLUG = 'tour'
NAME = 'Tour / Official Duty Management'
FEATURES = ('Tour Dashboard', 'Apply Tour', 'My Tour Applications', 'Tour Approval', 'Tour Rejection', 'Tour Cancellation', 'Tour History', 'Tour Calendar', 'Tour Expense Estimate', 'Tour Documents', 'Tour Reports')
SIDEBAR = ('Apply Tour', 'My Tour Applications', 'Tour Approval', 'Tour Reports')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
