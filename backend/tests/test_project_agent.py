import copy
import json
from types import SimpleNamespace

import pytest
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function

from app.agent.project_agent import FALLBACK_REPLY, MAX_TOOL_ROUNDS, ProjectAgent
from app.agent.tools import ProjectTools
from app.models.chat import ChatMessage
from app.models.enums import MessageRole, ProjectCategory
from app.services.project_repository import ProjectRepository

TEST_PROJECTS = [
    {"id": 1, "name": "Haifa Park", "city": "חיפה", "categories": ["residential"], "url": "https://example.com/1"},
]


class FakeOpenAI:
    """Looks like the OpenAI client from the outside, but returns scripted responses and records every call."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls.append(copy.deepcopy(kwargs))  # copy: the agent keeps changing the same messages list
        message = self._responses.pop(0) if self._responses else tool_call("search_projects", "{}")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def text(content):
    return ChatCompletionMessage(role="assistant", content=content)


def tool_call(name, arguments):
    return ChatCompletionMessage(
        role="assistant",
        content=None,
        tool_calls=[ChatCompletionMessageToolCall(
            id="call_1", type="function", function=Function(name=name, arguments=arguments),
        )],
    )


@pytest.fixture
def tools(tmp_path):
    projects_file = tmp_path / "projects.json"
    projects_file.write_text(json.dumps(TEST_PROJECTS), encoding="utf-8")
    return ProjectTools(ProjectRepository(projects_file))


def ask(agent, question="מחפש דירה בחיפה"):
    return agent.reply(ProjectCategory.RESIDENTIAL, [ChatMessage(role=MessageRole.USER, text=question)])


def test_plain_text_answer_is_returned(tools):
    client = FakeOpenAI([text("שלום!")])
    assert ask(ProjectAgent(client, "fake-model", tools)) == "שלום!"
    assert len(client.calls) == 1


def test_tool_is_run_and_result_sent_back_to_model(tools):
    client = FakeOpenAI([tool_call("search_projects", '{"city": "חיפה"}'), text("מצאתי את Haifa Park")])
    answer = ask(ProjectAgent(client, "fake-model", tools))

    assert answer == "מצאתי את Haifa Park"
    second_call_messages = client.calls[1]["messages"]
    tool_message = second_call_messages[-1]
    assert tool_message["role"] == "tool"
    assert tool_message["tool_call_id"] == "call_1"
    assert "Haifa Park" in tool_message["content"]
    # The model's own tool request must be in the history right before the tool result.
    assert second_call_messages[-2]["tool_calls"][0]["id"] == "call_1"


def test_loop_stops_after_max_rounds(tools):
    client = FakeOpenAI([])  # with no scripted answers, the fake keeps asking for tools forever
    assert ask(ProjectAgent(client, "fake-model", tools)) == FALLBACK_REPLY
    assert len(client.calls) == MAX_TOOL_ROUNDS


def test_system_prompt_and_roles(tools):
    client = FakeOpenAI([text("ok")])
    conversation = [
        ChatMessage(role=MessageRole.BOT, text="מה חשוב לך?"),
        ChatMessage(role=MessageRole.USER, text="פארק"),
    ]
    ProjectAgent(client, "fake-model", tools).reply(ProjectCategory.RENTAL, conversation)

    messages = client.calls[0]["messages"]
    assert messages[0]["role"] == "system"
    assert "rental" in messages[0]["content"]
    assert [m["role"] for m in messages[1:]] == ["assistant", "user"]
