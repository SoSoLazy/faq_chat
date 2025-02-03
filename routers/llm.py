from fastapi import APIRouter

from schemas.llm_model import ChatSessionIn, ChatSessionOut
from services.llm_service import LLMService

router = APIRouter()

@router.post("/chat_session")
def chat_session(chat_in: ChatSessionIn) -> ChatSessionOut:
    return LLMService.get_instance().chat_session(chat_in.message, chat_in.session_id)