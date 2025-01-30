from typing import Optional

import os
import logging

from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class OpenAiCLient:
    """
    openAI와 api를 통해 통신하는 클라이언트 클래스 입니다.
    """
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def chat_completions(self, message: str, chat_history: Optional[str]=None, retrival_result: Optional[str]=None) -> str:
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
        logging.info(response)

        return response.choices[0].message.content
    
    def embedding(self, message:str) -> str:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=message
        )
        logging.info(message, response)

        return response.data[0].embedding

open_ai_client = OpenAiCLient(OPENAI_API_KEY)