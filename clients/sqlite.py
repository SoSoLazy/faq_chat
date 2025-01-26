from typing import Optional

import sqlite3
from threading import Lock

# TODO: 더 효율적인 방법으로 데이터를 가져오도록 바꾸기
class SQLiteClient:
    def __init__(self, db_path):
        self.db_path = db_path
        self.lock = Lock()  # 스레드 안전을 위한 락

    def _get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def execute_query(self, query, params=None, commit=False):
        with self.lock:  # 스레드 안전 보장
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                if commit:
                    conn.commit()
                return cursor.fetchall()

    def create_table(self, table_name, columns):
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute_query(sql, commit=True)

    def insert_data(self, table_name, data):
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.execute_query(sql, params=data, commit=True)

    
    def read_data(self, table_name, session_id:Optional[str]=None):
        sql = f"SELECT * FROM {table_name}"
        
        if session_id:
            sql += f'\nWHERE session_id = "{session_id}"'

        return self.execute_query(sql)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
