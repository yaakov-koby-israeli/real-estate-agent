from enum import StrEnum


class ProjectCategory(StrEnum):
    RESIDENTIAL = "residential"
    RENTAL = "rental"
    URBAN_RENEWAL = "urban_renewal"


class ProjectStatus(StrEnum):
    MARKETING = "marketing"
    FUTURE = "future"
    POPULATED = "populated"


class ProjectFeature(StrEnum):
    PARK = "park"
    SEA = "sea"
    SCHOOLS = "schools"
    TRANSPORT = "transport"
    SHOPPING = "shopping"
    TENANTS_CLUB = "tenants_club"
    PARKING = "parking"


class ChatStep(StrEnum):
    CHOOSE_TYPE = "choose_type"
    ASK_NAME = "ask_name"
    ASK_PHONE = "ask_phone"
    ASK_PREFERENCES = "ask_preferences"
    AGENT_CONVERSATION = "agent_conversation"
    ASK_CALLBACK = "ask_callback"
    DONE = "done"


class MessageRole(StrEnum):
    USER = "user"
    BOT = "bot"
