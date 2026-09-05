"""Device and security management module."""
SLUG = 'security'
NAME = 'Device & Security Management'
FEATURES = ('Registered Devices', 'Trusted Devices', 'Device Approval', 'Device Blocking', 'IP Whitelist', 'IP Blacklist', 'Login Security', 'Failed Login Attempts', 'Account Lockout', 'Active Sessions', 'JWT Token Management', 'Refresh Token Management', 'Security Logs')
SIDEBAR = ('Registered Devices', 'Active Sessions', 'Login History', 'Security Logs')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
