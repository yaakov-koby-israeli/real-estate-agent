import pytest

from app.models.chat import ChatSession
from app.models.enums import ChatStep, MessageRole, ProjectCategory
from app.services.chat_flow import FINISH_OPTION
from tests.conftest import FAKE_AGENT_ANSWER


@pytest.fixture
def session(flow):
    session = ChatSession(id="test")
    flow.start(session)
    return session


def reach_agent_conversation(flow, session, preferences="3 חדרים בתל אביב"):
    flow.handle_message(session, "דיור להשכרה")
    flow.handle_message(session, "יעקב")
    flow.handle_message(session, "050-1234567")
    return flow.handle_message(session, preferences)


def test_start_offers_type_options(flow):
    reply = flow.start(ChatSession(id="new"))
    assert reply.options == ["מגורים", "דיור להשכרה"]


def test_full_happy_path(flow, session):
    reach_agent_conversation(flow, session)
    flow.handle_message(session, FINISH_OPTION)
    flow.handle_message(session, "כן, אשמח שיחזרו אליי")

    assert session.step == ChatStep.DONE
    assert session.category == ProjectCategory.RENTAL
    assert session.name == "יעקב"
    assert session.phone == "0501234567"
    assert session.preferences == "3 חדרים בתל אביב"
    assert session.wants_callback is True


def test_preferences_are_answered_by_agent(flow, session, fake_agent):
    reply = reach_agent_conversation(flow, session)

    assert session.step == ChatStep.AGENT_CONVERSATION
    assert reply.text == FAKE_AGENT_ANSWER
    assert reply.options == [FINISH_OPTION]
    assert fake_agent.calls == [(ProjectCategory.RENTAL, ["3 חדרים בתל אביב"])]


def test_agent_never_sees_name_or_phone(flow, session, fake_agent):
    reach_agent_conversation(flow, session)
    flow.handle_message(session, "ומה עם 4 חדרים?")

    _, conversation = fake_agent.calls[-1]
    assert conversation == ["3 חדרים בתל אביב", FAKE_AGENT_ANSWER, "ומה עם 4 חדרים?"]
    assert not any("יעקב" in text or "050" in text for text in conversation)


def test_agent_conversation_excludes_everything_after_finish(flow, session):
    reach_agent_conversation(flow, session)
    flow.handle_message(session, FINISH_OPTION)
    flow.handle_message(session, "כן, אשמח שיחזרו אליי")

    # The closing message contains name and phone - it must stay out of what we send to OpenAI.
    texts = [m.text for m in session.agent_conversation()]
    assert texts == ["3 חדרים בתל אביב", FAKE_AGENT_ANSWER]
    assert not any("יעקב" in t or "0501234567" in t for t in texts)


def test_follow_up_questions_stay_with_agent(flow, session, fake_agent):
    reach_agent_conversation(flow, session)
    flow.handle_message(session, "ומה עם 4 חדרים?")
    assert session.step == ChatStep.AGENT_CONVERSATION
    assert len(fake_agent.calls) == 2


def test_finish_moves_to_callback_question(flow, session):
    reach_agent_conversation(flow, session)
    reply = flow.handle_message(session, FINISH_OPTION)
    assert session.step == ChatStep.ASK_CALLBACK
    assert "כן, אשמח שיחזרו אליי" in reply.options


def test_lead_is_saved_once_when_conversation_ends(flow, session, fake_lead_service):
    reach_agent_conversation(flow, session)
    flow.handle_message(session, FINISH_OPTION)
    assert fake_lead_service.saved == []

    flow.handle_message(session, "לא, תודה")
    flow.handle_message(session, "עוד הודעה אחרי הסיום")

    assert len(fake_lead_service.saved) == 1
    saved = fake_lead_service.saved[0]
    assert saved.wants_callback is False
    assert saved.history[-1].role == MessageRole.BOT  # the closing message is already in the transcript


def test_unknown_type_stays_on_same_step(flow, session):
    reply = flow.handle_message(session, "משרדים")
    assert session.step == ChatStep.CHOOSE_TYPE
    assert reply.options


def test_invalid_name_stays_on_same_step(flow, session):
    flow.handle_message(session, "מגורים")
    flow.handle_message(session, "123")
    assert session.step == ChatStep.ASK_NAME
    assert session.name is None


def test_invalid_phone_stays_on_same_step(flow, session):
    flow.handle_message(session, "מגורים")
    flow.handle_message(session, "יעקב")
    flow.handle_message(session, "12345")
    assert session.step == ChatStep.ASK_PHONE

    flow.handle_message(session, "0521234567")
    assert session.step == ChatStep.ASK_PREFERENCES


def test_history_records_both_sides(flow, session):
    flow.handle_message(session, "מגורים")
    roles = [m.role for m in session.history]
    assert roles == [MessageRole.BOT, MessageRole.USER, MessageRole.BOT]
