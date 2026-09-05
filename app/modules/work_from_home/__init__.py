"""Work from home management module."""
SLUG = 'work-from-home'
NAME = 'Work From Home Management'
FEATURES = ('WFH Dashboard', 'Apply Work From Home', 'My WFH Applications', 'WFH Approval', 'WFH Rejection', 'WFH Cancellation', 'WFH Calendar', 'WFH Check-In', 'WFH Check-Out', 'Daily Work Report', 'Task / Work Update', 'WFH Reports')
SIDEBAR = ('Apply Work From Home', 'My WFH Applications', 'WFH Approval', 'Daily Work Report', 'WFH Reports')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' / ', '-').replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
