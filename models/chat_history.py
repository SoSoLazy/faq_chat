from sqlmodel import Field, SQLModel

class ChatHistory(SQLModel, table=True):
    __tablename__ = "chat_history"
    session_id: str = Field(description="챗 히스토리 저장, 조회를 위한 session id", index=True)
    chat_history_list: str | None = Field(description="챗 히스토리 이력", unique=True, index=True)
