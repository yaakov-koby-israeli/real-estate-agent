"""Scrape Prashkovsky projects and save them to data/projects.json.

Run from the backend folder:  python -m scripts.run_scraper
"""
import json
from collections import Counter
from pathlib import Path

from app.scraper.prashkovsky_scraper import PrashkovskyScraper

OUTPUT_FILE = Path(__file__).parent.parent / "data" / "projects.json"


def main():
    projects = PrashkovskyScraper().scrape_projects()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = [project.model_dump(mode="json") for project in projects]
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = Counter(category for project in projects for category in project.categories)
    print(f"Saved {len(projects)} projects to {OUTPUT_FILE}")
    for category, count in counts.items():
        print(f"  {category}: {count}")


if __name__ == "__main__":
    main()
