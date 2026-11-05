import pytest

from app.models.chat import ChatSession
from app.models.enums import ChatStep, MessageRole, ProjectCategory
from app.services.chat_flow import ChatFlow


@pytest.fixture
def flow():
    return ChatFlow()


@pytest.fixture
def session(flow):
    session = ChatSession(id="test")
    flow.start(session)
    return session


def test_start_offers_type_options(flow):
    reply = flow.start(ChatSession(id="new"))
    assert reply.options == ["מגורים", "דיור להשכרה"]


def test_full_happy_path(flow, session):
    flow.handle_message(session, "דיור להשכרה")
    flow.handle_message(session, "יעקב")
    flow.handle_message(session, "050-1234567")
    flow.handle_message(session, "3 חדרים בתל אביב")
    flow.handle_message(session, "כן, אשמח שיחזרו אליי")

    assert session.step == ChatStep.DONE
    assert session.category == ProjectCategory.RENTAL
    assert session.name == "יעקב"
    assert session.phone == "0501234567"
    assert session.preferences == "3 חדרים בתל אביב"
    assert session.wants_callback is True


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
