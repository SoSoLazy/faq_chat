from fastapi import APIRouter

from schemas.llm_model import ChatBaseModel
from services.llm_service import LLMService

router = APIRouter()

@router.post("/chat")
def chat(chat_in: ChatBaseModel):
    return LLMService.get_instance().chat_one_time(chat_in.message)

@router.post("/chat_session")
def chat_session(chat_in: ChatBaseModel):
    return LLMService.get_instance().chat_session(chat_in.message, chat_in.session_id)