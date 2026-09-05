"""AI and attendance anomaly management module."""
SLUG = 'ai-anomalies'
NAME = 'AI & Anomaly Management'
FEATURES = ('Attendance Anomaly Dashboard', 'Suspicious Attendance', 'Duplicate Attendance Detection', 'Face Mismatch Detection', 'Location Anomaly', 'Impossible Travel Detection', 'Unusual Attendance Pattern', 'AI Risk Score', 'Anomaly Investigation', 'Resolve Anomaly', 'AI Settings')
SIDEBAR = ('Attendance Anomaly Dashboard', 'Suspicious Attendance', 'Face Mismatch Detection', 'Anomaly Investigation', 'AI Settings')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
