from typing import Optional, List, Dict

import os
import json

from clients.open_ai import open_ai_client
from services.session_service import SessionService
from schemas.chat_history import ChatHistory, ChatHistoryList

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class LLMService:
    """
    메인 서비스!
    - 채팅 관리
    - 세션 관리
    """

    def __init__(self, session_service: SessionService):
        self.session_service = session_service

    def chat_one_time(self, message:str):
        session_id = self.session_service.generate_session_id()

        chat = open_ai_client.chat_completions(message=message)
        
        chat_history = ChatHistory.model_validate({
            "request": message,
            "response": chat
        })

        self.session_service.upsert_chat_history(
            session_id, chat_history_list=ChatHistoryList.model_validate(
                {
                    "chat_history_list": list(chat_history)
                }
            )
        )
        return chat

    def chat_session(self, message:str, session_id: Optional[str]):
        if (session_id is None):
            session_id = self.session_service.generate_session_id()
            chat_history_list: List[Dict] = [] 
        elif not (past_data := self.session_service.get_chat_history(session_id=session_id)):
            chat_history_list = [] 
        else:                                                                 
            past_chat_history_list = json.loads(past_data[0][1])
            chat_history_list = past_chat_history_list["chat_history_list"]
            
            messages_with_session = ""
            for chat_history_raw in chat_history_list:
                messages_with_session += f"\nQ : {chat_history_raw["request"]}"
                messages_with_session += f"\nA : {chat_history_raw["response"]}"
            messages_with_session += f"\nQ : {message}"
            
        response = open_ai_client.chat_completions(message=message)

        chat_history = {
            "request": message,
            "response": response
        }
        chat_history_list.append(chat_history)
        
        self.session_service.upsert_chat_history(
            session_id, chat_history_list=ChatHistoryList.model_validate({
                "chat_history_list": chat_history_list
            })
        )
        
        return {
            "response": response,
            "session_id": session_id
        }
