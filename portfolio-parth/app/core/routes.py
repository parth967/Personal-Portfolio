"""
Core portfolio routes
"""
from flask import Blueprint, render_template

core_bp = Blueprint('core', __name__,
                     template_folder='templates',
                     static_folder='static')

@core_bp.route('/')
def core_home():
    """Main portfolio page."""
    # For now, return empty data array since blog functionality is disabled
    data = []
    return render_template('index.html', data=data)

@core_bp.route('/home')
def core_home2():
    """Alternative home route."""
    return render_template('index.html', data=[])