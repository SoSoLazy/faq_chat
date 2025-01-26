from fastapi import APIRouter
from services.llm_service import LLMService

from schemas.llm_model import ChatBaseModel
from services.session_service import session_service

router = APIRouter()
llm_service = LLMService(session_service=session_service)


@router.post("/chat")
def chat(chat_in: ChatBaseModel):
    return llm_service.chat_one_time(chat_in.message)

@router.post("/chat_session")
def chat_session(chat_in: ChatBaseModel):
    return llm_service.chat_session(chat_in.message, chat_in.session_id)