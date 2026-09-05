"""
Audit Service — helper to log actions throughout the app.
"""
from flask import request as flask_request
from app.extensions import db
from app.models.audit_log import AuditLog


class AuditService:
    """Creates audit log entries for critical actions."""

    @staticmethod
    def log(
        action: str,
        module: str = None,
        user_id: int = None,
        organization_id: int = None,
        record_type: str = None,
        record_id: int = None,
        old_data: dict = None,
        new_data: dict = None,
        description: str = None,
        ip_address: str = None,
    ):
        try:
            ip = ip_address or (flask_request.remote_addr if flask_request else None)
            ua = flask_request.headers.get('User-Agent') if flask_request else None

            entry = AuditLog(
                organization_id=organization_id,
                user_id=user_id,
                action=action,
                module=module,
                record_type=record_type,
                record_id=record_id,
                old_data=old_data,
                new_data=new_data,
                description=description,
                ip_address=ip,
                user_agent=ua,
            )
            db.session.add(entry)
            db.session.commit()
        except Exception as e:
            # Never let audit logging break the main flow
            db.session.rollback()
            import logging
            logging.getLogger(__name__).error(f'Audit log failed: {e}')
