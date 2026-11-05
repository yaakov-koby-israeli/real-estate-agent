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
