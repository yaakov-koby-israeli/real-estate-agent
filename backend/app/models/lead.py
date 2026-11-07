from datetime import datetime

from pydantic import BaseModel

from app.models.chat import ChatMessage
from app.models.enums import InterestLevel, ProjectCategory, ProjectFeature


class LeadSummary(BaseModel):
    """Extracted from the conversation by the AI. Structured fields make demand analysis possible."""

    summary: str
    requested_cities: list[str]  # free text on purpose - cities we have no project in are valuable insight
    requested_rooms: list[int]
    requested_features: list[ProjectFeature]
    suggested_projects: list[str]
    interest_level: InterestLevel


class Lead(BaseModel):
    """What the sales team receives at the end of a conversation."""

    session_id: str
    created_at: datetime
    name: str
    phone: str
    category: ProjectCategory
    wants_callback: bool
    preferences: str | None
    summary: LeadSummary | None  # None if the AI summary failed - the lead is still saved
    transcript: list[ChatMessage]
