from fastapi import APIRouter
from backend.app.schemas.auth import ChatRequest, ChatResponse
from backend.app.services.chat_service import chat_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat_with_assistant(data: ChatRequest):
    history_dicts = [h.model_dump() for h in data.history] if data.history else None
    result = chat_service.reply(data.message, history=history_dicts)
    return ChatResponse(
        reply=result["reply"],
        sources=result.get("sources", []),
        search_performed=result.get("search_performed", False)
    )
