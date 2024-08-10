import re
from datetime import datetime
import sshtunnel
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

DATA_FILE_LOC = 'sample.txt'
DB_TOTAL_LIMIT = 10000
ROW_LIMIT = 1000
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0
current_date = datetime.now().date()
only_current_day = False
load_dotenv()

def read_logs(file_path):
    date_pattern = r'\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\]'
    browser_pattern = r'\((.*?)\)'
    ip_pattern = r'(\d+\.\d+\.\d+\.\d+)'
    date_regex = re.compile(date_pattern)
    browser_regex = re.compile(browser_pattern)
    ip_regex = re.compile(ip_pattern)
    log_list = []
    try:
        with open(file_path, 'r') as file:
            for log in file:
                date = None
                browser = None
                ip = None

                date_match = date_regex.search(log)
                browser_match = browser_regex.search(log)
                ip_match = ip_regex.search(log)

                date = date_match.group(1) if date_match else ''
                browser = browser_match.group(1) if browser_match else ''
                ip = ip_match.group(1) if ip_match else ''

                log_list.append({
                    'date': date,
                    'browser': browser,
                    'ip': ip
                })
        return log_list
    except Exception as e:
        print(e)
        return []

def get_day_logs(date, logs):
    day_logs = []
    for log in logs:
        date_string = log.get('date', None)
        if date_string:
            parsed_date = datetime.strptime(date_string, "%d/%b/%Y:%H:%M:%S %z")
            parsed_date_date = parsed_date.date()
            if parsed_date_date >= date:
                day_logs.append(log)
    return day_logs

def clean_log_json(logs):
    clean_logs = {}
    if isinstance(logs, list):
        unique_ip = []
        for log in logs:
            current_ip = str(log.get('ip',''))
            if current_ip in unique_ip:
                clean_logs[current_ip]['count'] = clean_logs[current_ip]['count'] + 1
            else:
                log.update({'count':1})
                clean_logs[current_ip] = log
                unique_ip.append(current_ip)
    return clean_logs

def build_insert_statement(logs):
    insert_statement = f''' INSERT INTO access_logs(timestamp, ip_address, user_agent, count)
                            VALUES 
                        '''
    total_len = len(logs)
    count = 0
    for log in logs:
        u_log = logs.get(log)
        count = count + 1
        values = f''' ('{u_log.get('date')}', '{u_log.get('ip')}', '{u_log.get('browser')}', '{u_log.get('count')}')'''
        if count == total_len:
            values = values + ';'
        else:
            values = values + ','
        insert_statement = insert_statement + values

    return insert_statement

def execute_db(query, is_return=False):
    conn = None
    result = None
    with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                                       ssh_username='Parth967', 
                                       ssh_password='Parth25111997',
                                       remote_bind_address=('Parth967.mysql.pythonanywhere-services.com', 3306)
                                     ) as tunnel:
        conn = pymysql.connect(host='127.0.0.1',
                             user='Parth967',
                             password='Parth25111997',
                             database='Parth967$default',
                             port=tunnel.local_bind_port,
                             cursorclass=pymysql.cursors.DictCursor)
        with conn.cursor() as cursor:
            cursor.execute(query)
            if is_return:
                result = cursor.fetchone()
        conn.commit()
        conn.close()

    return result

logs = read_logs(DATA_FILE_LOC)
filter_logs = get_day_logs(current_date, logs) if only_current_day else logs
clean_logs = clean_log_json(logs)

total_count = int(execute_db('SELECT count(*) as total_rows FROM access_logs', True).get('total_rows'))

if total_count < DB_TOTAL_LIMIT and len(clean_logs) < ROW_LIMIT:
    limited_logs = clean_logs[:ROW_LIMIT] if len(clean_logs) > ROW_LIMIT else clean_logs
    insert_statement = build_insert_statement(limited_logs)
    print(f'----- {len(limited_logs)} logs added')
    execute_db(insert_statement)