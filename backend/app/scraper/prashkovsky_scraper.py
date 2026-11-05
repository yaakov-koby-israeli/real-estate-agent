import time

import requests

from app.models.project import Project
from app.scraper.project_parser import parse_project

API_URL = "https://www.prashkovsky.co.il/wp-json/wp/v2"
PAGE_SIZE = 100
REQUEST_DELAY_SECONDS = 1
USER_AGENT = "real-estate-agent-bot/0.1 (internal demo)"


class PrashkovskyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT

    def _get_all_pages(self, endpoint: str) -> list[dict]:
        items = []
        page = 1
        while True:
            response = self.session.get(
                f"{API_URL}/{endpoint}",
                params={"per_page": PAGE_SIZE, "page": page},
                timeout=30,
            )
            response.raise_for_status()
            batch = response.json()
            items.extend(batch)
            if len(batch) < PAGE_SIZE:
                return items
            page += 1
            time.sleep(REQUEST_DELAY_SECONDS)

    def fetch_category_slugs(self) -> dict[int, str]:
        """Map WordPress term id -> slug, e.g. {13: 'home', 16: 'rent'}."""
        terms = self._get_all_pages("project_category")
        return {term["id"]: term["slug"] for term in terms}

    def fetch_raw_projects(self) -> list[dict]:
        return self._get_all_pages("project")

    def scrape_projects(self) -> list[Project]:
        """Fetch all projects and keep only the ones relevant to private customers."""
        category_slugs = self.fetch_category_slugs()
        projects = [parse_project(raw, category_slugs) for raw in self.fetch_raw_projects()]
        return [project for project in projects if project is not None]
