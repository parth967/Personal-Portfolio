from flask import Flask
from .core.routes import core_bp
from flask_jwt_extended import JWTManager
from .dashboard.routes import dash_bp
from .blogs.routes import blog_bp
import  sshtunnel 
from .extension import db
from sqlalchemy import create_engine, Table, MetaData, select
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    sshtunnel.SSH_TIMEOUT = 5.0
    sshtunnel.TUNNEL_TIMEOUT = 5.0
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    jwt = JWTManager(app)
    app.register_blueprint(core_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(blog_bp)
    return app