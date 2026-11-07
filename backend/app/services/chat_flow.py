from app.agent.project_agent import ProjectAgent
from app.models.chat import ChatMessage, ChatReply, ChatSession
from app.models.enums import ChatStep, MessageRole, ProjectCategory
from app.services.lead_service import LeadService
from app.services.validation import normalize_name, normalize_phone

# Button label -> value. The frontend sends back the exact label the user clicked.
TYPE_OPTIONS = {
    "מגורים": ProjectCategory.RESIDENTIAL,
    "דיור להשכרה": ProjectCategory.RENTAL,
}
CALLBACK_OPTIONS = {
    "כן, אשמח שיחזרו אליי": True,
    "לא, תודה": False,
}
FINISH_OPTION = "סיימתי, תודה"
CALLBACK_QUESTION = "האם תרצה/י שנציג ממחלקת המכירות יחזור אליך להמשך התהליך?"


class ChatFlow:
    """Deterministic conversation: each step has one handler that validates input and picks the next step.
    Only the free-text part (preferences and follow-up questions) is handed to the AI agent."""

    def __init__(self, agent: ProjectAgent, lead_service: LeadService):
        self._agent = agent
        self._lead_service = lead_service
        self._handlers = {
            ChatStep.CHOOSE_TYPE: self._handle_choose_type,
            ChatStep.ASK_NAME: self._handle_name,
            ChatStep.ASK_PHONE: self._handle_phone,
            ChatStep.ASK_PREFERENCES: self._handle_preferences,
            ChatStep.AGENT_CONVERSATION: self._handle_agent_conversation,
            ChatStep.ASK_CALLBACK: self._handle_callback,
            ChatStep.DONE: self._handle_done,
        }

    def start(self, session: ChatSession) -> ChatReply:
        reply = ChatReply(
            text="שלום! אני הסוכן הווירטואלי של פרשקובסקי 🏠 אשמח לעזור לך למצוא את הבית הבא שלך. מה מעניין אותך?",
            options=list(TYPE_OPTIONS),
        )
        self._record(session, MessageRole.BOT, reply.text)
        return reply

    def handle_message(self, session: ChatSession, text: str) -> ChatReply:
        step_before = session.step
        self._record(session, MessageRole.USER, text)
        reply = self._handlers[session.step](session, text.strip())
        self._record(session, MessageRole.BOT, reply.text)
        # Save the lead exactly once - when the conversation has just finished, with the full transcript.
        if session.step == ChatStep.DONE and step_before != ChatStep.DONE:
            self._lead_service.save(session)
        return reply

    def _record(self, session: ChatSession, role: MessageRole, text: str):
        session.history.append(ChatMessage(role=role, text=text))

    def _handle_choose_type(self, session: ChatSession, text: str) -> ChatReply:
        category = TYPE_OPTIONS.get(text)
        if category is None:
            return ChatReply(text="אנא בחר/י אחת מהאפשרויות:", options=list(TYPE_OPTIONS))
        session.category = category
        session.step = ChatStep.ASK_NAME
        return ChatReply(text="מעולה! איך קוראים לך?")

    def _handle_name(self, session: ChatSession, text: str) -> ChatReply:
        name = normalize_name(text)
        if name is None:
            return ChatReply(text="לא הצלחתי להבין את השם. אנא כתוב/י שם באותיות בלבד (לפחות 2 אותיות).")
        session.name = name
        session.step = ChatStep.ASK_PHONE
        return ChatReply(text=f"נעים מאוד {name}! מה מספר הטלפון הנייד שלך?")

    def _handle_phone(self, session: ChatSession, text: str) -> ChatReply:
        phone = normalize_phone(text)
        if phone is None:
            return ChatReply(text="המספר לא תקין. אנא הזן/י מספר נייד ישראלי, לדוגמה: 050-1234567")
        session.phone = phone
        session.step = ChatStep.ASK_PREFERENCES
        return ChatReply(
            text="תודה! ספר/י לי מה חשוב לך: באיזה אזור, כמה חדרים, קרבה לבתי ספר, לפארק, לים וכו'."
        )

    def _handle_preferences(self, session: ChatSession, text: str) -> ChatReply:
        session.preferences = text
        session.agent_start_index = len(session.history) - 1  # the preferences message we just recorded
        session.step = ChatStep.AGENT_CONVERSATION
        return self._ask_agent(session)

    def _handle_agent_conversation(self, session: ChatSession, text: str) -> ChatReply:
        if text == FINISH_OPTION:
            session.agent_end_index = len(session.history) - 1  # stop before the "finish" click
            session.step = ChatStep.ASK_CALLBACK
            return ChatReply(text=CALLBACK_QUESTION, options=list(CALLBACK_OPTIONS))
        return self._ask_agent(session)

    def _ask_agent(self, session: ChatSession) -> ChatReply:
        answer = self._agent.reply(session.category, session.agent_conversation())
        return ChatReply(text=answer, options=[FINISH_OPTION])

    def _handle_callback(self, session: ChatSession, text: str) -> ChatReply:
        wants_callback = CALLBACK_OPTIONS.get(text)
        if wants_callback is None:
            return ChatReply(text="אנא בחר/י אחת מהאפשרויות:", options=list(CALLBACK_OPTIONS))
        session.wants_callback = wants_callback
        session.step = ChatStep.DONE
        if wants_callback:
            return ChatReply(text=f"מצוין {session.name}! נציג יחזור אליך בהקדם למספר {session.phone}.")
        return ChatReply(text="בסדר גמור. תודה שפנית לפרשקובסקי, ואם תצטרך/י משהו - אני כאן!")

    def _handle_done(self, session: ChatSession, text: str) -> ChatReply:
        return ChatReply(text="השיחה הסתיימה. תודה שפנית לפרשקובסקי! 🏠")
