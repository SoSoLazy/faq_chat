from typing import Optional

import os

from openai import OpenAI
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
from config import RAG_EMBEDDING_SIZE

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

class OpenAiCLient:
    """
    openAI와 api를 통해 통신하는 클라이언트 클래스 입니다.
    """

    _instance = None
    
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY,
            model_name="text-embedding-3-small",
            dimensions=RAG_EMBEDDING_SIZE
        )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = OpenAiCLient(OPENAI_API_KEY)
        return cls._instance

    def chat_completions(self, message: str, chat_history: Optional[str]=None, retrival_result: Optional[str]=None) -> str:
        """
        1) 과거 채팅 기록과, 2) RAG 검색 결과를 참고해서, 3) 사용자 질문에 답변 해 주는 함수
        """
        # 0) 프롬프트 작성
        messages = [
            {"role": "system", "content": "사용자 질문에 답변해주세요."},
        ]

        # 1) 세션 프롬프트 추가
        if chat_history:
            messages.append(
                {"role": "assistant", "content": f"이전에 제공된 질문과 답변 : {chat_history}"}
            )

        # 2) RAG 프롬프트 추가
        if retrival_result:
            messages.append(
                {"role": "assistant", "content": f"질문의 검색 결과 : {retrival_result}"}
            )

        # 3) 사용자 질문 추가
        messages.append(
            {"role": "user", "content": message}
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return response.choices[0].message.content
    
    def chat_predict_next_question(self, chat_history) -> str:
        """
        사용자 문맥에서, 다음에 궁금한 아이템 검색
        """
        # 0) 프롬프트 작성
        messages = [
            {"role": "system", "content": "사용자의 채팅 히스토리에서, 다음에 궁금할 것을 알려주세요.\n설명과, 기타 이야기 없이 궁금해 할 내용만 요약해서 알려주세요."},
        ]

        # 1) 사용자 채팅 히스토리
        messages.append(
            {"role": "user", "content": chat_history}
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return response.choices[0].message.content
    
    def chat_make_next_question(self, chat_history, next_question, nums=5) -> str:
        """
        사용자 문맥과, 사용자가 질문할 것 같은 내용을 정리해서, n개의 다음 질문 목록을 생성
        """
        # 0) 프롬프트 작성
        messages = [
            {"role": "system", "content": f"사용자의 채팅 히스토리를 참고하여, 예상 질문 목록록 중 다음에 궁금할 내용 최대 {nums}개를 알려주세요.\n예상 질문만 한줄씩 \\n 으로 구분지어 답변 해 주세요. 다른 응답이 있으면 안됩니다."},
        ]

        # 1) 사용자 채팅 히스토리
        messages.append(
            {"role": "user", "content": f"채팅 히스토리 : {chat_history}"}
        )

        # 2) 예상 질문 목록
        messages.append(
            {"role": "user", "content": f"예상 질문 : {next_question}"}
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return response.choices[0].message.content
    
    def embedding(self, message:str) -> str:
        response = self.embedding_model([message])
        return response[0]
