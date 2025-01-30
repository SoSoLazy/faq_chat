from fastapi import APIRouter

from services.session_service import session_service
from services.rag_service import rag_service

router = APIRouter()

@router.get("/chat_histories")
def chat():
    return session_service.get_chat_history()

@router.post("/rag_retrival")
def rag_retrical(input_dict: dict):
    return rag_service.search(input_dict["message"])
