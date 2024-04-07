from flask import Blueprint, render_template
                                  
core_bp = Blueprint('core', __name__,
                     template_folder='templates',
                     static_folder='static')

@core_bp.route('/')
def core_home():
    return render_template('index.html')

@core_bp.route('/home')
def core_home2():
    return render_template('index.html')