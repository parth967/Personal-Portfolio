from flask import Flask
from .core.routes import core_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(core_bp)
    return app