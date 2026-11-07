import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_chat_flow, get_session_store
from app.main import app
from app.services.session_store import SessionStore


@pytest.fixture
def client(flow):
    store = SessionStore()  # fresh, empty store for every test
    app.dependency_overrides[get_session_store] = lambda: store
    app.dependency_overrides[get_chat_flow] = lambda: flow  # flow with FakeAgent, from conftest.py
    yield TestClient(app)
    app.dependency_overrides.clear()


def send(client, session_id, message):
    return client.post("/api/chat/message", json={"session_id": session_id, "message": message})


def test_start_returns_session_and_options(client):
    data = client.post("/api/chat/start").json()
    assert data["session_id"]
    assert data["step"] == "choose_type"
    assert data["options"] == ["מגורים", "דיור להשכרה"]


def test_conversation_advances_steps(client):
    session_id = client.post("/api/chat/start").json()["session_id"]
    assert send(client, session_id, "מגורים").json()["step"] == "ask_name"
    assert send(client, session_id, "יעקב").json()["step"] == "ask_phone"


def test_unknown_session_returns_404(client):
    assert send(client, "does-not-exist", "שלום").status_code == 404


def test_empty_message_is_rejected(client):
    session_id = client.post("/api/chat/start").json()["session_id"]
    assert send(client, session_id, "").status_code == 422


def test_too_long_message_is_rejected(client):
    session_id = client.post("/api/chat/start").json()["session_id"]
    assert send(client, session_id, "א" * 1001).status_code == 422
