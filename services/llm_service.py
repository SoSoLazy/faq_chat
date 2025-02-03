from typing import Optional, List, Dict

import json

from clients.open_ai import OpenAiCLient
from services.session_service import SessionService
from services.rag_service import RagService
from schemas.chat_history import ChatHistory, ChatHistoryList
from schemas.llm_model import ChatSessionOut
from config import LLM_THRESHOLD_FOR_VALID_REQUEST, LLM_SESSION_LIMIT_FOR_CHAT, LLM_NONE_FAQ_REQUEST_MESSAGE

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

    def chat_session(self, message:str, session_id: Optional[str]) -> ChatSessionOut:
        messages_with_session = ""

        # 1: 세션 관리
        # 1-1) session_id 가 none 인 경우 세션 생성
        if (session_id is None):
            session_id = self.session_service.generate_session_id()
            chat_history_list: List[Dict] = [] 
        # 1-2) 과거 데이터가 없는 경우
        elif not (past_data := self.session_service.get_chat_history(session_id=session_id)):
            chat_history_list = [] 
        # 1-3) 과거 데이터가 있는 경우, 프롬프트 생성
        else:
            past_chat_history_list = json.loads(past_data[0][1])
            chat_history_list = past_chat_history_list["chat_history_list"]
            
            for chat_history_raw in chat_history_list[-LLM_SESSION_LIMIT_FOR_CHAT:]:
                messages_with_session += f"\n질문 : {chat_history_raw["request"]}"
                messages_with_session +=  f"\n응답 : {chat_history_raw["response"]}"

        # 2: 스마트 스토어와 무관한 질문을 하는지 확인
        # "현재 들어온 질문"이 스마트 스토어와 관계 없는 질문이 들어온 경우, 답변 회피
        retrival_for_now_message = self.rag_service.search_by_message(
            message
        )
        if min(retrival_for_now_message["distances"][0]) >= LLM_THRESHOLD_FOR_VALID_REQUEST:
            response_message = LLM_NONE_FAQ_REQUEST_MESSAGE
            metadata_list = []
        else:
            retrival_for_all_messages = self.rag_service.search_by_message(
                f"{messages_with_session}\n질문 : {message}"
            )

            # 3: RAG 검색 및 응답
            retrival_prompt = " ".join(retrival_for_all_messages["documents"][0])
            response_message = self.open_ai_client.chat_completions(
                message=message, 
                chat_history=messages_with_session,
                retrival_result=retrival_prompt,
            )

            metadata_list = retrival_for_all_messages["metadatas"][0]

        # 4: 현재 세션의 채팅 결과를 다시 DB에 저장
        chat_history = {
            "request": message,
            "response": response_message
        }
        chat_history_list.append(chat_history)
        
        self.session_service.upsert_chat_history(
            session_id, chat_history_list=ChatHistoryList.model_validate({
                "chat_history_list": chat_history_list
            })
        )

        # 5: 응답 결과와 RAG 결과를 사용해서 사용자가 궁금해할만한 다른 내용 검색
        # 5-1) 채팅 히스토리에서 사용자가 궁금해 할 질문 검색 (LLM + RAG)
        all_chat_histories = messages_with_session + f"\n질문: {message} \n응답: {response_message}"
        next_question = self.open_ai_client.chat_predict_next_question(all_chat_histories)
        retrival_data_for_next_question = self.rag_service.search_by_message(next_question)
        nest_question_list = [
            next_question.split("응답")[0].strip() for next_question in retrival_data_for_next_question["documents"][0]
        ]

        # 5-2) RAG 결과의 additional question 추출
        nest_question_list += [
            metadata.get("additional_request") for metadata in metadata_list
            if metadata.get("additional_request")
        ]

        # 5-3) 위 두 결과를 통합하여, 다음에 질문할 목록 생성
        additional_questions = self.open_ai_client.chat_make_next_question(
            chat_history=chat_history,
            next_question=", ".join(nest_question_list),
            nums=5
        )

        return ChatSessionOut.model_validate(
            {
                "message": response_message,
                "session_id": session_id,
                "additional_questions": [
                    additional_question.replace("질문:", "").strip() for additional_question in additional_questions.split('\n')
                ],
            }
        )
