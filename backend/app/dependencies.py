from functools import lru_cache

from openai import OpenAI

from app.agent.lead_summarizer import LeadSummarizer
from app.agent.project_agent import ProjectAgent
from app.agent.tools import ProjectTools
from app.config import LEADS_DIR, OPENAI_API_KEY, OPENAI_MODEL, PROJECTS_FILE
from app.services.chat_flow import ChatFlow
from app.services.lead_service import LeadService
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
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)


@lru_cache
def get_project_agent() -> ProjectAgent:
    return ProjectAgent(get_openai_client(), OPENAI_MODEL, ProjectTools(get_project_repository()))


@lru_cache
def get_lead_service() -> LeadService:
    return LeadService(LeadSummarizer(get_openai_client(), OPENAI_MODEL), LEADS_DIR)


@lru_cache
def get_chat_flow() -> ChatFlow:
    return ChatFlow(get_project_agent(), get_lead_service())
