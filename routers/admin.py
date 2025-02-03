from fastapi import APIRouter

from services.session_service import SessionService
from services.rag_service import RagService

router = APIRouter()

@router.get("/chat_histories")
def chat():
    return SessionService.get_instance().get_chat_history()

@router.post("/rag_retrival")
def rag_retrical(input_dict: dict):
    return RagService.get_instance().search_by_message(input_dict["message"])
