"""System settings module."""
SLUG = 'settings'
NAME = 'System Settings'
FEATURES = ('My Profile', 'General Settings', 'Company Settings', 'Attendance Settings', 'Face Recognition Settings', 'CCTV Settings', 'Geo Attendance Settings', 'Leave Settings', 'Notification Settings', 'Email Settings', 'SMS Settings', 'WhatsApp Settings', 'JWT Settings', 'Security Settings', 'Backup Settings')
SIDEBAR = ('My Profile', 'General Settings', 'Attendance Settings', 'Face Recognition Settings', 'CCTV Settings', 'Geo Attendance Settings', 'Notification Settings', 'Security Settings')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
