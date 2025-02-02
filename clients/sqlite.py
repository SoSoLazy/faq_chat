from typing import Optional, Dict, Any

import sqlite3
from threading import Lock

class SQLiteClient:
    def __init__(self, db_path):
        self.db_path = db_path
        self.lock = Lock()

    def _get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def execute_query(self, query, params=None, commit=False):
        with self.lock:
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

    def upsert_data(self, table_name, data: Dict[str, Any], conflict_column: str):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        updates = ', '.join([f"{col} = excluded.{col}" for col in data.keys()])
        
        sql = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        ON CONFLICT({conflict_column}) DO UPDATE SET {updates};
        """

        self.execute_query(sql, params=list(data.values()), commit=True)

    def read_data(self, table_name, session_id: Optional[str] = None):
        sql = f"SELECT * FROM {table_name}"
        params = []
        if session_id:
            sql += "\nWHERE session_id = ?"
            params.append(session_id)
        return self.execute_query(sql, params=params)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
