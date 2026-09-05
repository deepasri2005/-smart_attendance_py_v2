"""Face recognition management module."""
SLUG = 'face-ai'
NAME = 'Face Recognition Management'
FEATURES = ('Face Registration', 'Face Profile Management', 'Face Image Management', 'Face Encoding Management', 'Face Verification', 'Face Recognition Logs', 'Liveness Detection', 'Anti-Spoofing', 'Unknown Face Detection', 'Face Recognition Settings')
SIDEBAR = ('Face Profile Management', 'Face Encoding Management', 'Liveness Detection', 'Face Recognition Logs', 'Unknown Face Detection')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
