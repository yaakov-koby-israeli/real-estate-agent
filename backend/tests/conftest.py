"""Shared test helpers. pytest loads this file automatically - fixtures here are available to every test."""
import pytest

from app.services.chat_flow import ChatFlow

FAKE_AGENT_ANSWER = "תשובה מהסוכן"


class FakeAgent:
    """Stands in for ProjectAgent: no OpenAI calls, just records what it was asked."""

    def __init__(self):
        self.calls = []

    def reply(self, category, conversation):
        self.calls.append((category, [m.text for m in conversation]))
        return FAKE_AGENT_ANSWER


@pytest.fixture
def fake_agent():
    return FakeAgent()


@pytest.fixture
def flow(fake_agent):
    return ChatFlow(fake_agent)
