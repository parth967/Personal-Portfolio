"""
Portfolio Flask Application
"""
import os
from flask import Flask, request
from dotenv import load_dotenv
from .core.routes import core_bp

load_dotenv()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    app.register_blueprint(core_bp)

    @app.after_request
    def add_cache_control(response):
        # Long cache for static assets — site can handle more visitors (fewer origin hits)
        if request.path.startswith('/static/'):
            response.cache_control.public = True
            response.cache_control.max_age = 604800  # 7 days
        return response

    return app