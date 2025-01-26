from typing import List

from pydantic import BaseModel


class ChatHistory(BaseModel):
    request: str
    response: str

class ChatHistoryList(BaseModel):
    chat_history_list: List[ChatHistory]