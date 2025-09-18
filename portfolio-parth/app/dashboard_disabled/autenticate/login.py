from flask_jwt_extended import JWTManager, create_access_token, decode_token
from flask import Flask, render_template, request, jsonify
from ...model.User import User
from datetime import timedelta

def authenticate_user(username, password):
    user = User()
    user_varified = user.verify_user(username, password)
    if user_varified:
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
    else:
        access_token = None
    return access_token

def decode_jwt_token(access_token):
    try:
        decoded_token = decode_token(access_token)
        return decoded_token
    except Exception as e:
        print(e)
        return None