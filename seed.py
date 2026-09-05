"""Initialize the existing Codevocado database and synchronize RBAC."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.extensions import db
from app.models.role import Role
from app.services.module_catalog_service import sync_module_catalog

app = create_app(os.environ.get('FLASK_ENV', 'development'))


def seed_database():
    """Synchronize RBAC records in the existing imported database."""
    with app.app_context():
        sync_module_catalog()

        print('Database and RBAC catalog synchronized successfully.')


if __name__ == '__main__':
    seed_database()
