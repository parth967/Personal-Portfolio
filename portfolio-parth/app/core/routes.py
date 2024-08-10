from flask import Blueprint, render_template
from ..blogs.routes import basic_blog_info
                                  
core_bp = Blueprint('core', __name__,
                     template_folder='templates',
                     static_folder='static')

@core_bp.route('/')
def core_home():
    data = basic_blog_info()
    return render_template('index.html', data=data)

@core_bp.route('/home')
def core_home2():
    return render_template('index.html')