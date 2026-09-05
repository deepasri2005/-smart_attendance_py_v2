"""
Main / Public Routes Blueprint — home page, features, about
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Public landing page."""
    return render_template('main/home.html')


@main_bp.route('/features')
def features():
    return render_template('main/home.html', scroll_to='features')


@main_bp.route('/about')
def about():
    return render_template('main/home.html', scroll_to='about')


@main_bp.route('/contact')
def contact():
    return render_template('main/home.html', scroll_to='contact')
