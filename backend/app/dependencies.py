from functools import lru_cache

from app.config import PROJECTS_FILE
from app.services.chat_flow import ChatFlow
from app.services.project_repository import ProjectRepository
from app.services.session_store import SessionStore


@lru_cache
def get_project_repository() -> ProjectRepository:
    """Created once on first use, then the same instance is reused for every request."""
    return ProjectRepository(PROJECTS_FILE)


@lru_cache
def get_session_store() -> SessionStore:
    return SessionStore()


@lru_cache
def get_chat_flow() -> ChatFlow:
    return ChatFlow()
