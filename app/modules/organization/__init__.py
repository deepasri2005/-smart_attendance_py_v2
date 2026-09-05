"""Organization management module."""
SLUG = 'organization'
NAME = 'Organization Management'
FEATURES = ('Organization Profile', 'Department Management', 'Designation Management', 'Organization Locations', 'Holiday Management', 'Week-Off Management', 'Organization Policies')
SIDEBAR = ('Organization Profile', 'Department Management', 'Designation Management', 'Organization Locations', 'Holiday Management', 'Week-Off Management', 'Organization Policies')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' & ', '-').replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
