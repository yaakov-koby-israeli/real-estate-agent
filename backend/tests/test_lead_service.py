import json

from app.models.chat import ChatMessage, ChatSession
from app.models.enums import ChatStep, InterestLevel, MessageRole, ProjectCategory
from app.models.lead import LeadSummary
from app.services.lead_service import LeadService

SUMMARY = LeadSummary(
    summary="מחפשים 5 חדרים", requested_cities=["מודיעין"], requested_rooms=[5],
    requested_features=[], suggested_projects=[], interest_level=InterestLevel.MEDIUM,
)


class FakeSummarizer:
    def __init__(self, result=SUMMARY):
        self.result = result
        self.conversations = []

    def summarize(self, category, conversation):
        self.conversations.append([m.text for m in conversation])
        return self.result


def finished_session(agent_start_index=2):
    return ChatSession(
        id="abc123", step=ChatStep.DONE, category=ProjectCategory.RESIDENTIAL,
        name="דנה לוי", phone="0547654321", preferences="5 חדרים", wants_callback=True,
        agent_start_index=agent_start_index, agent_end_index=4,
        history=[
            ChatMessage(role=MessageRole.USER, text="דנה לוי"),
            ChatMessage(role=MessageRole.USER, text="0547654321"),
            ChatMessage(role=MessageRole.USER, text="5 חדרים"),
            ChatMessage(role=MessageRole.BOT, text="מצאתי לך..."),
            ChatMessage(role=MessageRole.USER, text="סיימתי, תודה"),
            ChatMessage(role=MessageRole.BOT, text="מצוין דנה לוי! נציג יחזור למספר 0547654321."),
        ],
    )


def test_lead_is_written_to_json_file(tmp_path):
    LeadService(FakeSummarizer(), tmp_path).save(finished_session())

    files = list(tmp_path.glob("*.json"))
    assert len(files) == 1
    assert files[0].name.endswith("_abc123.json")
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["phone"] == "0547654321"
    assert data["summary"]["requested_cities"] == ["מודיעין"]
    assert len(data["transcript"]) == 6  # the saved file keeps everything - it never leaves our server


def test_summarizer_gets_only_the_agent_conversation(tmp_path):
    summarizer = FakeSummarizer()
    LeadService(summarizer, tmp_path).save(finished_session())
    assert summarizer.conversations == [["5 חדרים", "מצאתי לך..."]]


def test_lead_is_saved_even_if_summary_fails(tmp_path):
    lead = LeadService(FakeSummarizer(result=None), tmp_path).save(finished_session())
    assert lead.summary is None
    assert len(list(tmp_path.glob("*.json"))) == 1


def test_no_agent_conversation_means_no_summary_call(tmp_path):
    summarizer = FakeSummarizer()
    lead = LeadService(summarizer, tmp_path).save(finished_session(agent_start_index=None))
    assert lead.summary is None
    assert summarizer.conversations == []
