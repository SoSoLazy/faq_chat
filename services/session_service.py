from typing import Optional, List

import pendulum
import random
import string

from clients.sqlite import SQLiteClient
from schemas.chat_history import ChatHistoryList
from config import SESSION_TABLE_NAME, SESSION_DB_PATH, SESSION_CONFLICT_COLUMNS, SESSION_COLUMNS


class SessionService:
    """
    세션 관리 서비스
    sqlite client 에 접근하여 채팅 내역을 관리하여 세션별 채팅을 지속할 수 있도록 해 줍니다.    
    """

    _instance = None

    def __init__(self, db_path):
        self.sqlite_client = SQLiteClient(db_path)
        self.sqlite_client.create_table(SESSION_TABLE_NAME, SESSION_COLUMNS)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SessionService(SESSION_DB_PATH)
        return cls._instance


    def generate_session_id(self) -> str:
        now = pendulum.now('UTC')
        timestamp = now.to_iso8601_string()
        random_string = ''.join(random.choices(string.ascii_letters, k=5))

        return f"{timestamp}_{random_string}"

    def upsert_chat_history(self, session_id:str, chat_history_list: ChatHistoryList):
        
        self.sqlite_client.upsert_data(
            SESSION_TABLE_NAME, 
            {
                "session_id": session_id,
                "chat_history_list": chat_history_list.model_dump_json(),
            },
            conflict_column=SESSION_CONFLICT_COLUMNS
        )

    def get_chat_history(self, session_id:Optional[str] = None) -> List:
        return self.sqlite_client.read_data(SESSION_TABLE_NAME, session_id)
