"""Metadata and navigation API for all application modules."""
from flask import Blueprint, jsonify
from app.decorators.auth import login_required
from app.modules import MODULES, get_module, permission_actions, sidebar_modules

modules_bp = Blueprint('modules', __name__, url_prefix='/api/modules')


@modules_bp.get('')
@login_required
def list_modules():
    """List registered modules, features, and supported permission actions."""
    return jsonify({
        'success': True,
        'modules': list(MODULES.values()),
        'permission_actions': permission_actions(),
    })


@modules_bp.get('/sidebar')
@login_required
def sidebar():
    """Return the compact sidebar menu used by dashboard clients."""
    return jsonify({'success': True, 'modules': sidebar_modules()})


@modules_bp.get('/<slug>')
@login_required
def module_detail(slug):
    """Return one module definition for a module landing page."""
    module = get_module(slug)
    if module is None:
        return jsonify({'success': False, 'message': 'Module not found'}), 404
    return jsonify({'success': True, 'module': module, 'permission_actions': permission_actions()})


@modules_bp.get('/<slug>/<feature_slug>')
@login_required
def feature_detail(slug, feature_slug):
    """Return one executable feature contract for a frontend or service."""
    module = get_module(slug)
    if module is None:
        return jsonify({'success': False, 'message': 'Module not found'}), 404

    feature = next((item for item in module['features'] if item['slug'] == feature_slug), None)
    if feature is None:
        return jsonify({'success': False, 'message': 'Feature not found'}), 404
    return jsonify({
        'success': True,
        'module': slug,
        'feature': feature,
        'permission_actions': permission_actions(),
    })
