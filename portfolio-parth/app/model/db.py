import pymysql
import os
import pymysql.cursors
from . import ssh

def build_connection(tunnel):
    conn = pymysql.connect(host=os.getenv('LOCAL_HOST'),
                               user=os.getenv('DB_USER'),
                               password=os.getenv('DB_PASSWORD'),
                               database=os.getenv('DB_NAME'),
                               port=tunnel.local_bind_port,
                               cursorclass=pymysql.cursors.DictCursor)
    return conn