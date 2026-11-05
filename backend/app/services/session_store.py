import uuid

from app.models.chat import ChatSession


class SessionStore:
    """Keeps chat sessions in memory. They are lost when the server restarts - fine for this demo."""

    def __init__(self):
        self._sessions: dict[str, ChatSession] = {}

    def create(self) -> ChatSession:
        session = ChatSession(id=uuid.uuid4().hex)
        self._sessions[session.id] = session
        return session

    def get(self, session_id: str) -> ChatSession | None:
        return self._sessions.get(session_id)
