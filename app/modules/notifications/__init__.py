"""Notification management module."""
SLUG = 'notifications'
NAME = 'Notification Management'
FEATURES = ('Notification Dashboard', 'My Notifications', 'Send Notification', 'Announcement Management', 'Attendance Alerts', 'Leave Notifications', 'Approval Notifications', 'Email Notifications', 'SMS Notifications', 'WhatsApp Notifications', 'Notification Templates', 'Notification History')
SIDEBAR = ('My Notifications', 'Send Notification', 'Announcement Management', 'Notification Templates')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
