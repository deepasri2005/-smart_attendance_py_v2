"""
Organization Blueprint Routes — Complete CRUD API for Organization & sub-entities
"""
from datetime import datetime
from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.decorators.auth import login_required
from app.models.organization import Organization
from app.models.employee import (
    Department, Designation, OrganizationLocation,
    Holiday, WeekOffRule, AttendanceRule
)
from app.models.audit_log import AuditLog

organization_bp = Blueprint('organization_api', __name__, url_prefix='/api/organization')


def _get_target_org_id(data=None):
    user = g.current_user
    if not user.is_super_admin:
        return user.organization_id or 1
    if data and data.get('organization_id'):
        return int(data.get('organization_id'))
    req_org = request.args.get('organization_id', type=int)
    if req_org:
        return req_org
    return user.organization_id or 1


# ─── 1. ORGANIZATION PROFILE & SETTINGS ───────────────────────────────────────

@organization_bp.get('/profile')
@login_required
def get_profile():
    org_id = _get_target_org_id()
    org = db.session.get(Organization, org_id)
    if not org:
        return jsonify({'success': False, 'message': 'Organization not found'}), 404
    
    return jsonify({
        'success': True,
        'organization': org.to_dict(),
        'details': {
            'email': org.email,
            'phone': org.phone,
            'address': org.address,
            'city': org.city,
            'state': org.state,
            'country': org.country,
            'postal_code': org.postal_code,
            'website': org.website,
            'logo': org.logo,
        }
    })


@organization_bp.put('/profile')
@organization_bp.post('/profile')
@login_required
def update_profile():
    org_id = _get_target_org_id()
    org = db.session.get(Organization, org_id)
    if not org:
        return jsonify({'success': False, 'message': 'Organization not found'}), 404

    data = request.get_json() or request.form
    if 'name' in data and data['name']:
        org.name = data['name'].strip()
    if 'email' in data:
        org.email = data['email'].strip()
    if 'phone' in data:
        org.phone = data['phone'].strip()
    if 'address' in data:
        org.address = data['address'].strip()
    if 'city' in data:
        org.city = data['city'].strip()
    if 'state' in data:
        org.state = data['state'].strip()
    if 'country' in data:
        org.country = data['country'].strip()
    if 'postal_code' in data:
        org.postal_code = data['postal_code'].strip()
    if 'website' in data:
        org.website = data['website'].strip()

    org.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Organization profile updated successfully',
        'organization': org.to_dict()
    })


# ─── 2. DEPARTMENTS CRUD ──────────────────────────────────────────────────────

@organization_bp.get('/departments')
@login_required
def list_departments():
    org_id = _get_target_org_id()
    depts = Department.query.filter_by(organization_id=org_id).all()
    return jsonify({'success': True, 'departments': [d.to_dict() for d in depts]})


@organization_bp.post('/departments')
@login_required
def create_department():
    data = request.get_json() or request.form
    name = (data.get('name') or data.get('department_name') or '').strip()
    code = (data.get('code') or data.get('department_code') or '').strip()
    description = (data.get('description') or '').strip()

    if not name:
        return jsonify({'success': False, 'message': 'Department name is required'}), 400

    org_id = _get_target_org_id(data)
    dept = Department(
        organization_id=org_id,
        name=name,
        code=code or None,
        description=description or None,
        is_active=True
    )
    db.session.add(dept)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Department created successfully', 'department': dept.to_dict()}), 201


@organization_bp.put('/departments/<int:dept_id>')
@login_required
def update_department(dept_id):
    dept = db.session.get(Department, dept_id)
    if not dept:
        return jsonify({'success': False, 'message': 'Department not found'}), 404

    data = request.get_json() or request.form
    if 'name' in data and data['name']:
        dept.name = data['name'].strip()
    if 'code' in data:
        dept.code = data['code'].strip() or None
    if 'description' in data:
        dept.description = data['description'].strip() or None
    if 'is_active' in data:
        dept.is_active = bool(data['is_active'])

    dept.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Department updated successfully', 'department': dept.to_dict()})


@organization_bp.delete('/departments/<int:dept_id>')
@login_required
def delete_department(dept_id):
    dept = db.session.get(Department, dept_id)
    if not dept:
        return jsonify({'success': False, 'message': 'Department not found'}), 404

    db.session.delete(dept)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Department deleted successfully'})


# ─── 3. DESIGNATIONS CRUD ─────────────────────────────────────────────────────

@organization_bp.get('/designations')
@login_required
def list_designations():
    org_id = _get_target_org_id()
    desigs = Designation.query.filter_by(organization_id=org_id).all()
    return jsonify({'success': True, 'designations': [d.to_dict() for d in desigs]})


@organization_bp.post('/designations')
@login_required
def create_designation():
    data = request.get_json() or request.form
    name = (data.get('name') or data.get('designation_name') or '').strip()
    dept_id = data.get('department_id')
    description = (data.get('description') or '').strip()

    if not name:
        return jsonify({'success': False, 'message': 'Designation name is required'}), 400

    org_id = _get_target_org_id(data)
    desig = Designation(
        organization_id=org_id,
        department_id=int(dept_id) if dept_id else None,
        name=name,
        description=description or None,
        is_active=True
    )
    db.session.add(desig)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Designation created successfully', 'designation': desig.to_dict()}), 201


@organization_bp.put('/designations/<int:desig_id>')
@login_required
def update_designation(desig_id):
    desig = db.session.get(Designation, desig_id)
    if not desig:
        return jsonify({'success': False, 'message': 'Designation not found'}), 404

    data = request.get_json() or request.form
    if 'name' in data and data['name']:
        desig.name = data['name'].strip()
    if 'department_id' in data:
        desig.department_id = int(data['department_id']) if data['department_id'] else None
    if 'description' in data:
        desig.description = data['description'].strip() or None
    if 'is_active' in data:
        desig.is_active = bool(data['is_active'])

    db.session.commit()
    return jsonify({'success': True, 'message': 'Designation updated successfully', 'designation': desig.to_dict()})


@organization_bp.delete('/designations/<int:desig_id>')
@login_required
def delete_designation(desig_id):
    desig = db.session.get(Designation, desig_id)
    if not desig:
        return jsonify({'success': False, 'message': 'Designation not found'}), 404

    db.session.delete(desig)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Designation deleted successfully'})


# ─── 4. LOCATIONS CRUD ────────────────────────────────────────────────────────

@organization_bp.get('/locations')
@login_required
def list_locations():
    org_id = _get_target_org_id()
    locs = OrganizationLocation.query.filter_by(organization_id=org_id).all()
    return jsonify({'success': True, 'locations': [l.to_dict() for l in locs]})


@organization_bp.post('/locations')
@login_required
def create_location():
    data = request.get_json() or request.form
    name = (data.get('location_name') or data.get('name') or '').strip()
    address = (data.get('address') or '').strip()
    lat = data.get('latitude', 0.0)
    lng = data.get('longitude', 0.0)
    radius = data.get('allowed_radius_meters', 100)

    if not name:
        return jsonify({'success': False, 'message': 'Location name is required'}), 400

    org_id = _get_target_org_id(data)
    loc = OrganizationLocation(
        organization_id=org_id,
        location_name=name,
        address=address or None,
        latitude=float(lat),
        longitude=float(lng),
        allowed_radius_meters=int(radius),
        is_active=True
    )
    db.session.add(loc)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Location created successfully', 'location': loc.to_dict()}), 201


@organization_bp.put('/locations/<int:loc_id>')
@login_required
def update_location(loc_id):
    loc = db.session.get(OrganizationLocation, loc_id)
    if not loc:
        return jsonify({'success': False, 'message': 'Location not found'}), 404

    data = request.get_json() or request.form
    if 'location_name' in data or 'name' in data:
        loc.location_name = (data.get('location_name') or data.get('name')).strip()
    if 'address' in data:
        loc.address = data['address'].strip() or None
    if 'latitude' in data:
        loc.latitude = float(data['latitude'])
    if 'longitude' in data:
        loc.longitude = float(data['longitude'])
    if 'allowed_radius_meters' in data:
        loc.allowed_radius_meters = int(data['allowed_radius_meters'])
    if 'is_active' in data:
        loc.is_active = bool(data['is_active'])

    db.session.commit()
    return jsonify({'success': True, 'message': 'Location updated successfully', 'location': loc.to_dict()})


@organization_bp.delete('/locations/<int:loc_id>')
@login_required
def delete_location(loc_id):
    loc = db.session.get(OrganizationLocation, loc_id)
    if not loc:
        return jsonify({'success': False, 'message': 'Location not found'}), 404

    db.session.delete(loc)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Location deleted successfully'})


# ─── 5. HOLIDAYS CRUD ─────────────────────────────────────────────────────────

@organization_bp.get('/holidays')
@login_required
def list_holidays():
    org_id = _get_target_org_id()
    holidays = Holiday.query.filter_by(organization_id=org_id).order_by(Holiday.holiday_date.asc()).all()
    return jsonify({
        'success': True,
        'holidays': [{
            'id': h.id,
            'name': h.name,
            'holiday_date': h.holiday_date.isoformat(),
            'holiday_type': h.holiday_type,
            'description': h.description,
            'is_optional': h.is_optional,
        } for h in holidays]
    })


@organization_bp.post('/holidays')
@login_required
def create_holiday():
    data = request.get_json() or request.form
    name = (data.get('name') or data.get('holiday_name') or '').strip()
    h_date_str = data.get('holiday_date')
    h_type = data.get('holiday_type', 'ORG')
    description = (data.get('description') or '').strip()
    is_optional = bool(data.get('is_optional', False))

    if not name or not h_date_str:
        return jsonify({'success': False, 'message': 'Holiday name and date are required'}), 400

    try:
        h_date = datetime.strptime(h_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date format, expected YYYY-MM-DD'}), 400

    org_id = _get_target_org_id(data)
    holiday = Holiday(
        organization_id=org_id,
        name=name,
        holiday_date=h_date,
        holiday_type=h_type,
        description=description or None,
        is_optional=is_optional
    )
    db.session.add(holiday)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Holiday created successfully',
        'holiday': {
            'id': holiday.id,
            'name': holiday.name,
            'holiday_date': holiday.holiday_date.isoformat(),
            'holiday_type': holiday.holiday_type,
            'description': holiday.description,
            'is_optional': holiday.is_optional,
        }
    }), 201


@organization_bp.put('/holidays/<int:h_id>')
@login_required
def update_holiday(h_id):
    holiday = db.session.get(Holiday, h_id)
    if not holiday:
        return jsonify({'success': False, 'message': 'Holiday not found'}), 404

    data = request.get_json() or request.form
    if 'name' in data or 'holiday_name' in data:
        holiday.name = (data.get('name') or data.get('holiday_name')).strip()
    if 'holiday_date' in data and data['holiday_date']:
        try:
            holiday.holiday_date = datetime.strptime(data['holiday_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format'}), 400
    if 'holiday_type' in data:
        holiday.holiday_type = data['holiday_type']
    if 'description' in data:
        holiday.description = data['description'].strip() or None
    if 'is_optional' in data:
        holiday.is_optional = bool(data['is_optional'])

    db.session.commit()
    return jsonify({'success': True, 'message': 'Holiday updated successfully'})


@organization_bp.delete('/holidays/<int:h_id>')
@login_required
def delete_holiday(h_id):
    holiday = db.session.get(Holiday, h_id)
    if not holiday:
        return jsonify({'success': False, 'message': 'Holiday not found'}), 404

    db.session.delete(holiday)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Holiday deleted successfully'})


# ─── 6. WEEK-OFF RULES ────────────────────────────────────────────────────────

@organization_bp.get('/week-offs')
@login_required
def get_week_offs():
    org_id = _get_target_org_id()
    rules = WeekOffRule.query.filter_by(organization_id=org_id).all()
    return jsonify({
        'success': True,
        'week_offs': [{'id': r.id, 'day_of_week': r.day_of_week, 'is_active': r.is_active} for r in rules]
    })


@organization_bp.post('/week-offs')
@login_required
def save_week_offs():
    org_id = _get_target_org_id()
    data = request.get_json() or request.form
    days = data.get('days', [])  # list of int day_of_week e.g. [0, 6] for Sun/Sat

    # Clear existing rules for organization and replace
    WeekOffRule.query.filter_by(organization_id=org_id).delete()
    
    for day in days:
        rule = WeekOffRule(organization_id=org_id, day_of_week=int(day), is_active=True)
        db.session.add(rule)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Week-off configuration saved successfully'})


# ─── 7. ATTENDANCE POLICIES & RULES ───────────────────────────────────────────

@organization_bp.get('/rules')
@login_required
def get_attendance_rules():
    org_id = _get_target_org_id()
    rule = AttendanceRule.query.filter_by(organization_id=org_id).first()
    if not rule:
        # Create default attendance rule if not present
        rule = AttendanceRule(
            organization_id=org_id,
            minimum_working_hours=8.0,
            half_day_hours=4.0,
            late_grace_minutes=15,
            early_departure_minutes=15,
            cctv_cooldown_minutes=30,
            face_cooldown_minutes=10,
            geo_accuracy_limit_meters=100,
            allow_manual_attendance=True,
            require_face_liveness=False
        )
        db.session.add(rule)
        db.session.commit()

    return jsonify({
        'success': True,
        'rule': {
            'id': rule.id,
            'organization_id': rule.organization_id,
            'minimum_working_hours': rule.minimum_working_hours,
            'half_day_hours': rule.half_day_hours,
            'late_grace_minutes': rule.late_grace_minutes,
            'early_departure_minutes': rule.early_departure_minutes,
            'cctv_cooldown_minutes': rule.cctv_cooldown_minutes,
            'face_cooldown_minutes': rule.face_cooldown_minutes,
            'geo_accuracy_limit_meters': rule.geo_accuracy_limit_meters,
            'allowed_ips': rule.allowed_ips,
            'allow_manual_attendance': rule.allow_manual_attendance,
            'require_face_liveness': rule.require_face_liveness,
        }
    })


@organization_bp.post('/rules')
@organization_bp.put('/rules')
@login_required
def save_attendance_rules():
    org_id = _get_target_org_id()
    rule = AttendanceRule.query.filter_by(organization_id=org_id).first()
    if not rule:
        rule = AttendanceRule(organization_id=org_id)
        db.session.add(rule)

    data = request.get_json() or request.form
    if 'minimum_working_hours' in data:
        rule.minimum_working_hours = float(data['minimum_working_hours'])
    if 'half_day_hours' in data:
        rule.half_day_hours = float(data['half_day_hours'])
    if 'late_grace_minutes' in data:
        rule.late_grace_minutes = int(data['late_grace_minutes'])
    if 'early_departure_minutes' in data:
        rule.early_departure_minutes = int(data['early_departure_minutes'])
    if 'cctv_cooldown_minutes' in data:
        rule.cctv_cooldown_minutes = int(data['cctv_cooldown_minutes'])
    if 'face_cooldown_minutes' in data:
        rule.face_cooldown_minutes = int(data['face_cooldown_minutes'])
    if 'geo_accuracy_limit_meters' in data:
        rule.geo_accuracy_limit_meters = int(data['geo_accuracy_limit_meters'])
    if 'allowed_ips' in data:
        rule.allowed_ips = data['allowed_ips'].strip() or None
    if 'allow_manual_attendance' in data:
        rule.allow_manual_attendance = bool(data['allow_manual_attendance'])
    if 'require_face_liveness' in data:
        rule.require_face_liveness = bool(data['require_face_liveness'])

    rule.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({'success': True, 'message': 'Organization policies updated successfully'})
