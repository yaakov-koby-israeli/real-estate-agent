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
    # The slice of `history` that is the conversation with the AI agent: [start, end).
    # Anything outside it (name, phone, closing message) is never sent to OpenAI.
    agent_start_index: int | None = None
    agent_end_index: int | None = None

    def agent_conversation(self) -> list[ChatMessage]:
        if self.agent_start_index is None:
            return []
        return self.history[self.agent_start_index:self.agent_end_index]
