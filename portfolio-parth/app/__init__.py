"""
Portfolio Flask Application
"""
import os
from flask import Flask, redirect, request
from dotenv import load_dotenv
from .core.routes import core_bp

load_dotenv()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    app.register_blueprint(core_bp)

    @app.before_request
    def redirect_www_to_non_www():
        if request.host.startswith('www.'):
            new_host = request.host[4:]
            url = request.url.replace(request.host, new_host, 1)
            return redirect(url, code=301)

    return app