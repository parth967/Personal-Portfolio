from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, current_app
from .ssh import establish_ssh_tunnel
from .db import build_connection
import hashlib


class User:
    def __init__(self) -> None:
        self._currnt_retry_count = 0
        self._MAX_RETRY = 3
        pass

    def verify_user(self, username, password):
        user_exists = False
        try:
            with establish_ssh_tunnel() as tunnel:
                conn = build_connection(tunnel)
                with conn.cursor() as cursor:
                    password = self.hash_password(password)
                    user_exists = True if cursor.execute(f'''SELECT 1 FROM users WHERE username = '{username}' AND password = '{password}' ''') == 1 else False
            return user_exists
        except Exception as e:
            if 'Could not establish connection from local' in str(e) and self._currnt_retry_count > self._MAX_RETRY:
                self._currnt_retry_count = self._currnt_retry_count + 1
                return self.verify_user(username, password)
            else:
                return user_exists
        
    def hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()
