import os
from clients.open_ai import open_ai_client

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class LLMService:
    """
    메인 서비스!
    - 채팅 관리
    - 세션 관리
    """
    
    def one_time_chat(self, message:str):
        return open_ai_client.chat_completions(message=message)
