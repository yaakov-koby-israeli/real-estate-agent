import logging

from openai import OpenAI, OpenAIError

from app.agent.prompts import build_summary_prompt
from app.models.chat import ChatMessage
from app.models.enums import ProjectCategory
from app.models.lead import LeadSummary

logger = logging.getLogger(__name__)


class LeadSummarizer:
    """One OpenAI call that turns the conversation into a structured LeadSummary."""

    def __init__(self, client: OpenAI, model: str):
        self._client = client
        self._model = model

    def summarize(self, category: ProjectCategory, conversation: list[ChatMessage]) -> LeadSummary | None:
        transcript = "\n".join(f"{m.role}: {m.text}" for m in conversation)
        try:
            response = self._client.chat.completions.parse(
                model=self._model,
                messages=[
                    {"role": "system", "content": build_summary_prompt(category)},
                    {"role": "user", "content": transcript},
                ],
                response_format=LeadSummary,
            )
        except OpenAIError:
            logger.exception("Lead summary request failed")
            return None

        message = response.choices[0].message
        if message.parsed is None:
            logger.warning("Lead summary refused or empty: %s", message.refusal)
        return message.parsed
