from fastapi import APIRouter
from services.llm_service import LLMService

from models.llm_model import ChatBaseModel

router = APIRouter()
llm_service = LLMService()


@router.post("/chat")
def chat(chat_in: ChatBaseModel):
    return llm_service.one_time_chat(chat_in.message)
