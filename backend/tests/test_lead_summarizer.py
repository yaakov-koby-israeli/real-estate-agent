from types import SimpleNamespace

from openai import OpenAIError

from app.agent.lead_summarizer import LeadSummarizer
from app.models.chat import ChatMessage
from app.models.enums import InterestLevel, MessageRole, ProjectCategory
from app.models.lead import LeadSummary

CONVERSATION = [ChatMessage(role=MessageRole.USER, text="5 חדרים במודיעין")]

SUMMARY = LeadSummary(
    summary="מחפשים 5 חדרים במודיעין",
    requested_cities=["מודיעין"],
    requested_rooms=[5],
    requested_features=[],
    suggested_projects=[],
    interest_level=InterestLevel.HIGH,
)


def fake_client(parse):
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(parse=parse)))


def parsed_response(parsed, refusal=None):
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(parsed=parsed, refusal=refusal))])


def test_returns_parsed_summary_and_sends_transcript():
    calls = []

    def parse(**kwargs):
        calls.append(kwargs)
        return parsed_response(SUMMARY)

    result = LeadSummarizer(fake_client(parse), "fake-model").summarize(ProjectCategory.RESIDENTIAL, CONVERSATION)

    assert result == SUMMARY
    assert calls[0]["response_format"] is LeadSummary
    assert "5 חדרים במודיעין" in calls[0]["messages"][1]["content"]


def test_refusal_returns_none():
    client = fake_client(lambda **kwargs: parsed_response(None, refusal="I can't help with that"))
    assert LeadSummarizer(client, "fake-model").summarize(ProjectCategory.RESIDENTIAL, CONVERSATION) is None


def test_openai_error_returns_none():
    def parse(**kwargs):
        raise OpenAIError("network is down")

    assert LeadSummarizer(fake_client(parse), "fake-model").summarize(ProjectCategory.RESIDENTIAL, CONVERSATION) is None
