import html
import re

from bs4 import BeautifulSoup

from app.models.enums import ProjectCategory, ProjectFeature, ProjectStatus
from app.models.project import Project

# WordPress category slug -> our enums. Slugs not listed here (e.g. "invest") are ignored.
CATEGORY_BY_SLUG = {
    "home": ProjectCategory.RESIDENTIAL,
    "rent": ProjectCategory.RENTAL,
    "urban-renewal": ProjectCategory.URBAN_RENEWAL,
}

STATUS_BY_SLUG = {
    "marketing": ProjectStatus.MARKETING,
    "future": ProjectStatus.FUTURE,
    "populated": ProjectStatus.POPULATED,
}

KNOWN_CITIES = [
    "תל אביב", "ראשון לציון", "פתח תקווה", "רמת גן", "בת ים", "באר יעקב", "נס ציונה",
    "ראש העין", "גליל ים", "חיפה", "לוד", "הרצליה", "אשדוד", "רחובות", "נתניה",
    "רמלה", "חולון", "מודיעין", "אשקלון", "שהם", "מצליח",
]

FEATURE_KEYWORDS = {
    ProjectFeature.PARK: ["פארק", "גן ציבורי", "גינה ציבורית", "שטחים ירוקים"],
    # Phrases only: a short word like "הים" also matches inside other words ("הגבוהים").
    ProjectFeature.SEA: ["חוף הים", "חוף ים", "נוף לים", "נוף ים", "נוף הים", "טיילת"],
    ProjectFeature.SCHOOLS: ["בית ספר", "בתי ספר", "מוסדות חינוך", "מערכת חינוך", "גני ילדים"],
    ProjectFeature.TRANSPORT: ["רכבת", "תחבורה ציבורית", "תחנת"],
    ProjectFeature.SHOPPING: ["קניון", "מרכז מסחרי", "מרכזי קניות"],
    ProjectFeature.TENANTS_CLUB: ["מועדון דיירים"],
    ProjectFeature.PARKING: ["חניון", "חניה", "חנייה"],
}

# "3-5 חדרים" / "3–5 חד'"  and  "4 חדרים"
ROOMS_RANGE_PATTERN = re.compile(r"(\d)\s*[-–]\s*(\d)\s*חד")
ROOMS_SINGLE_PATTERN = re.compile(r"(\d)\s*חדרים")


def clean_html(raw_html: str) -> str:
    text = BeautifulSoup(raw_html, "html.parser").get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text)


def extract_city(title: str, description: str) -> str | None:
    for text in (title, description):
        for city in KNOWN_CITIES:
            if city in text:
                return city
    return None


def extract_rooms(description: str) -> list[int]:
    rooms = set()
    for start, end in ROOMS_RANGE_PATTERN.findall(description):
        rooms.update(range(int(start), int(end) + 1))
    for count in ROOMS_SINGLE_PATTERN.findall(description):
        rooms.add(int(count))
    return sorted(r for r in rooms if 1 <= r <= 7)


def extract_features(description: str) -> list[ProjectFeature]:
    return [
        feature
        for feature, keywords in FEATURE_KEYWORDS.items()
        if any(keyword in description for keyword in keywords)
    ]


def parse_project(raw: dict, category_slugs: dict[int, str]) -> Project | None:
    """Convert a raw WordPress project into our Project. Returns None if it's not relevant to us."""
    slugs = [category_slugs[term_id] for term_id in raw["project_category"]]
    categories = [CATEGORY_BY_SLUG[s] for s in slugs if s in CATEGORY_BY_SLUG]
    if not categories:
        return None

    status = next((STATUS_BY_SLUG[s] for s in slugs if s in STATUS_BY_SLUG), None)
    title = html.unescape(raw["title"]["rendered"]).strip()
    description = clean_html(raw["content"]["rendered"])
    og_images = raw.get("yoast_head_json", {}).get("og_image", [])

    return Project(
        id=raw["id"],
        name=title,
        city=extract_city(title, description),
        categories=categories,
        status=status,
        rooms=extract_rooms(description),
        features=extract_features(description),
        description=description,
        url=raw["link"],
        image_url=og_images[0]["url"] if og_images else None,
    )
