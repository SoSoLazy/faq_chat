from pydantic import BaseModel


class ChatBaseModel(BaseModel):
    message: str
