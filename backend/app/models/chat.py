from pydantic import BaseModel

from app.models.enums import ChatStep, MessageRole, ProjectCategory


class ChatMessage(BaseModel):
    role: MessageRole
    text: str


class ChatReply(BaseModel):
    text: str
    options: list[str] = []


class ChatSession(BaseModel):
    """Everything we know about one conversation. Data only - the logic lives in ChatFlow."""

    id: str
    step: ChatStep = ChatStep.CHOOSE_TYPE
    category: ProjectCategory | None = None
    name: str | None = None
    phone: str | None = None
    preferences: str | None = None
    wants_callback: bool | None = None
    history: list[ChatMessage] = []
