from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.dependencies import get_chat_flow, get_session_store
from app.models.chat import ChatReply, ChatSession
from app.models.enums import ChatStep
from app.services.chat_flow import ChatFlow
from app.services.session_store import SessionStore

router = APIRouter(prefix="/api/chat", tags=["chat"])


class MessageRequest(BaseModel):
    session_id: str
    message: str = Field(min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    session_id: str
    step: ChatStep
    text: str
    options: list[str]


def to_response(session: ChatSession, reply: ChatReply) -> ChatResponse:
    return ChatResponse(session_id=session.id, step=session.step, text=reply.text, options=reply.options)


@router.post("/start")
def start_chat(
    store: SessionStore = Depends(get_session_store),
    flow: ChatFlow = Depends(get_chat_flow),
) -> ChatResponse:
    session = store.create()
    return to_response(session, flow.start(session))


@router.post("/message")
def send_message(
    request: MessageRequest,
    store: SessionStore = Depends(get_session_store),
    flow: ChatFlow = Depends(get_chat_flow),
) -> ChatResponse:
    session = store.get(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return to_response(session, flow.handle_message(session, request.message))
