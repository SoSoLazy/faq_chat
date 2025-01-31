from typing import Optional, List, Dict

import os
import json

from clients.open_ai import OpenAiCLient
from services.session_service import SessionService
from services.rag_service import RagService
from schemas.chat_history import ChatHistory, ChatHistoryList

SESSION_LIMIT_FOR_CHAT = 8 # 응답에 활용하기 위한 과거 채팅 수
THRESHOLD_FOR_VALID_REQUEST = 1
NONE_FAQ_REQUEST_MESSAGE = "저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다."


class LLMService:
    """
    메인 서비스!
    - 채팅 관리
    - 세션 관리
    """

    _instance = None

    def __init__(self, session_service: SessionService, rag_service :RagService, open_ai_client: OpenAiCLient):
        self.session_service = session_service
        self.rag_service = rag_service
        self.open_ai_client = open_ai_client

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LLMService(
                session_service=SessionService.get_instance(),
                rag_service=RagService.get_instance(),
                open_ai_client=OpenAiCLient.get_instance(),
            )
        return cls._instance

    def chat_one_time(self, message:str):
        session_id = self.session_service.generate_session_id()

        chat = self.open_ai_client.chat_completions(message=message)
        
        chat_history = ChatHistory.model_validate({
            "request": message,
            "response": chat
        })
        chat_history_list = [chat_history]

        self.session_service.upsert_chat_history(
            session_id, chat_history_list=ChatHistoryList.model_validate({
                "chat_history_list": chat_history_list
            })
        )
        return chat

    def chat_session(self, message:str, session_id: Optional[str]):
        messages_with_session = ""

        # 1) session_id 가 none 인 경우 세션 생성
        if (session_id is None):
            session_id = self.session_service.generate_session_id()
            chat_history_list: List[Dict] = [] 
        # 2) 과거 데이터가 없는 경우
        elif not (past_data := self.session_service.get_chat_history(session_id=session_id)):
            chat_history_list = [] 
        # 3) 과거 데이터가 있는 경우, 프롬프트 생성
        else:
            past_chat_history_list = json.loads(past_data[0][1])
            chat_history_list = past_chat_history_list["chat_history_list"]
            
            for chat_history_raw in chat_history_list[-SESSION_LIMIT_FOR_CHAT:]:
                messages_with_session += f"\n질문 : {chat_history_raw["request"]}"
                messages_with_session +=  f"\n응답 : {chat_history_raw["response"]}"
        
        retrival_result = self.rag_service.search(message)

        # 스마트 스토어와 관계 없는 질문이 들어온 경우, 답변 회피
        if min(retrival_result["distances"]) >= THRESHOLD_FOR_VALID_REQUEST:
            return NONE_FAQ_REQUEST_MESSAGE

        retrival_prompt = " ".join(retrival_result["documents"][0])
        
        response = self.open_ai_client.chat_completions(
            message=message, 
            chat_history=messages_with_session,
            retrival_result=retrival_prompt,
        )

        chat_history = {
            "request": message,
            "response": response
        }
        chat_history_list.append(chat_history)
        
        # 채팅 결과를 다시 세션에 저장
        self.session_service.upsert_chat_history(
            session_id, chat_history_list=ChatHistoryList.model_validate({
                "chat_history_list": chat_history_list
            })
        )
        
        return {
            "response": response,
            "session_id": session_id
        }
