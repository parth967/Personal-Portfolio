from flask import Blueprint, render_template, jsonify, request, make_response, redirect, url_for, current_app, session
from .autenticate.login import authenticate_user, decode_jwt_token
from flask_jwt_extended import JWTManager, jwt_required
from ..model.Logs import Logs
import requests
from json import load

dash_bp = Blueprint('dash_bp', __name__,
                     template_folder='templates',
                     static_folder='static')



@dash_bp.route('/loginpage')
def dash_login_page():
    if request.cookies.get('access_token') and decode_jwt_token(request.cookies.get('access_token')):
        return redirect(url_for('dash_bp.dashboard'))
    else:
        return render_template('login.html')

@dash_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    access_token = authenticate_user(username, password)
    if not access_token:
        return jsonify({"msg": "Bad username or password"}), 401
    response = make_response(redirect(url_for('dash_bp.dashboard')))
    response.set_cookie('access_token', access_token)
    response.headers['Authorization'] = f'Bearer {access_token}'
    
    return response

@dash_bp.route('/dash', methods=['GET'])
def dashboard():
    access_token = request.cookies.get('access_token')
    if decode_jwt_token(access_token):
        log_c = Logs()
        log = log_c.get_logs() 
        return render_template('dashboard.html', data=log)
    else:
        return jsonify("Please Login")
