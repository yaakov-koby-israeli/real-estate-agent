from datetime import datetime
from pathlib import Path

from app.agent.lead_summarizer import LeadSummarizer
from app.models.chat import ChatSession
from app.models.lead import Lead


class LeadService:
    """Turns a finished conversation into a Lead and saves it as a JSON file for the sales team."""

    def __init__(self, summarizer: LeadSummarizer, leads_dir: Path):
        self._summarizer = summarizer
        self._leads_dir = leads_dir

    def save(self, session: ChatSession) -> Lead:
        lead = Lead(
            session_id=session.id,
            created_at=datetime.now().astimezone(),
            name=session.name,
            phone=session.phone,
            category=session.category,
            wants_callback=session.wants_callback,
            preferences=session.preferences,
            summary=self._summarize(session),
            transcript=session.history,
        )
        self._leads_dir.mkdir(parents=True, exist_ok=True)
        # No name/phone in the file name - file names end up in logs and backups.
        file_name = f"{lead.created_at:%Y%m%d-%H%M%S}_{session.id}.json"
        (self._leads_dir / file_name).write_text(lead.model_dump_json(indent=2), encoding="utf-8")
        return lead

    def _summarize(self, session: ChatSession):
        conversation = session.agent_conversation()
        if not conversation:
            return None
        return self._summarizer.summarize(session.category, conversation)
