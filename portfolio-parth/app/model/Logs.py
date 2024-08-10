from .ssh import establish_ssh_tunnel
from .db import build_connection
import hashlib
from datetime import datetime

class Logs:
    def __init__(self) -> None:
        self.DB_TOTAL_LIMIT = 10000
        self.ROW_LIMIT = 1000
        self.current_date = datetime.now().date()
        self.only_current_day = False
        self._currnt_retry_count = 0
        self._MAX_RETRY = 3

    def update_log_table(self):
        return 'Build in progress...'
    
    def get_logs(self):
        results = {}
        try:
            with establish_ssh_tunnel() as tunnel:
                conn = build_connection(tunnel)
                with conn.cursor() as cursor:
                    cursor.execute(f'''SELECT * FROM access_logs''')
                    results = cursor.fetchall()
            return results
        except Exception as e:
            if 'Could not establish connection from local' in str(e) and self._currnt_retry_count > self._MAX_RETRY:
                self._currnt_retry_count = self._currnt_retry_count + 1
                return self.get_logs()
            else:
                return results