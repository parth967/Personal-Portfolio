from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
import paramiko
from sshtunnel import SSHTunnelForwarder
import sshtunnel
from dotenv import load_dotenv
import os

load_dotenv()
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

def establish_ssh_tunnel():
    tunnel = SSHTunnelForwarder((os.getenv('SSH_HOST')),
        ssh_username=os.getenv('SSH_USERNAME'),
        ssh_password=os.getenv('SSH_PASSWORD'),
        remote_bind_address=(os.getenv('MYSQL_HOST'), int(os.getenv('MYSQL_PORT')))
    )
    tunnel.start()
    return tunnel
