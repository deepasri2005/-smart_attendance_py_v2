"""CCTV management module."""
SLUG = 'cctv'
NAME = 'CCTV Management'
FEATURES = ('CCTV Camera List', 'Add CCTV Camera', 'Edit CCTV Camera', 'Camera Locations', 'RTSP Configuration', 'Camera Status', 'Live Camera Monitoring', 'CCTV Detection Logs', 'Known Face Detection', 'Unknown Person Detection', 'CCTV Attendance Rules', 'CCTV Processing Settings')
SIDEBAR = ('CCTV Camera List', 'Live Camera Monitoring', 'CCTV Detection Logs', 'CCTV Processing Settings')

def get_definition():
    return {'slug': SLUG, 'name': NAME, 'features': [{'slug': item.lower().replace(' ', '-'), 'name': item, 'sidebar': item in SIDEBAR} for item in FEATURES]}
