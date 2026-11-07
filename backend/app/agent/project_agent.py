import logging

from openai import OpenAI, OpenAIError

from app.agent.prompts import build_system_prompt
from app.agent.tools import ProjectTools
from app.models.chat import ChatMessage
from app.models.enums import MessageRole, ProjectCategory

logger = logging.getLogger(__name__)

MAX_TOOL_ROUNDS = 4
FALLBACK_REPLY = "מצטער, לא הצלחתי למצוא תשובה כרגע. נציג מטעמנו ישמח לעזור לך באופן אישי."

OPENAI_ROLES = {MessageRole.USER: "user", MessageRole.BOT: "assistant"}


class ProjectAgent:
    """Talks to OpenAI and lets the model call our search tool until it has an answer."""

    def __init__(self, client: OpenAI, model: str, tools: ProjectTools):
        self._client = client
        self._model = model
        self._tools = tools

    def reply(self, category: ProjectCategory, conversation: list[ChatMessage]) -> str:
        messages = [{"role": "system", "content": build_system_prompt(category)}]
        messages += [{"role": OPENAI_ROLES[m.role], "content": m.text} for m in conversation]
        try:
            return self._run_tool_loop(messages)
        except OpenAIError:
            # Network / auth / rate-limit problems: the customer gets a polite reply, we get the details in the log.
            logger.exception("OpenAI request failed")
            return FALLBACK_REPLY

    def _run_tool_loop(self, messages: list[dict]) -> str:
        for _ in range(MAX_TOOL_ROUNDS):
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=self._tools.definitions(),
            )
            message = response.choices[0].message
            if not message.tool_calls:
                return message.content or FALLBACK_REPLY

            # The model asked for tools: keep its request in the history, run each tool, send results back.
            messages.append(message.model_dump(exclude_none=True))
            for call in message.tool_calls:
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": self._tools.run(call.function.name, call.function.arguments),
                })

        return FALLBACK_REPLY
