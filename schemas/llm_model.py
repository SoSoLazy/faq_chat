from typing import Optional

from pydantic import BaseModel


class ChatBaseModel(BaseModel):
    message: str # 채팅 메시지
    session_id: Optional[str] # 세션 관리를 위한 ID, ID가 없다면 신규 채팅으로 인식 됩니다.


class ChatSessionIn(ChatBaseModel):
    pass