from fastapi import APIRouter
from services.session_service import session_service

router = APIRouter()

@router.get("/chat_histories")
def chat():
    return session_service.get_chat_history()
