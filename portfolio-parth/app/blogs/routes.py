from flask import Blueprint, render_template
import os, json
                                  
blog_bp = Blueprint('blog', __name__,
                     template_folder='blogs_template',
                     static_folder='static')

def basic_blog_info():
    blog_config = f"{blog_bp.static_folder}/blog_info.json"
    blog_json = [{}]
    with open(blog_config) as data:
        blog_json = json.load(data)
    return blog_json

@blog_bp.route('/blog-builder')
def photon_vs_standard_db():
    return render_template('blogbuilder.html')