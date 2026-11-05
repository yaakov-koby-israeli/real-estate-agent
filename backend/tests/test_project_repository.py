import json

import pytest

from app.models.enums import ProjectCategory, ProjectFeature
from app.services.project_repository import ProjectRepository

TEST_PROJECTS = [
    {
        "id": 1, "name": "Haifa Park", "city": "חיפה", "categories": ["residential"],
        "rooms": [3, 4], "features": ["park", "sea"], "url": "https://example.com/1",
    },
    {
        "id": 2, "name": "Tel Aviv Rent", "city": "תל אביב", "categories": ["rental"],
        "rooms": [], "features": ["park"], "url": "https://example.com/2",
    },
    {
        "id": 3, "name": "Rehovot Tower", "city": "רחובות", "categories": ["residential", "urban_renewal"],
        "rooms": [5, 6], "features": [], "url": "https://example.com/3",
    },
]


@pytest.fixture
def repo(tmp_path):
    projects_file = tmp_path / "projects.json"
    projects_file.write_text(json.dumps(TEST_PROJECTS), encoding="utf-8")
    return ProjectRepository(projects_file)


def ids(projects):
    return [p.id for p in projects]


def test_no_filters_returns_all(repo):
    assert ids(repo.search()) == [1, 2, 3]


def test_search_by_category(repo):
    assert ids(repo.search(category=ProjectCategory.RESIDENTIAL)) == [1, 3]


def test_search_by_city(repo):
    assert ids(repo.search(city="חיפה")) == [1]


def test_known_rooms_that_dont_match_are_excluded(repo):
    assert 3 not in ids(repo.search(rooms=4))


def test_unknown_rooms_are_included(repo):
    assert 2 in ids(repo.search(rooms=4))


def test_features_must_all_match(repo):
    assert ids(repo.search(features=[ProjectFeature.PARK])) == [1, 2]
    assert ids(repo.search(features=[ProjectFeature.PARK, ProjectFeature.SEA])) == [1]


def test_no_match_returns_empty_list(repo):
    assert repo.search(city="אילת") == []


def test_cities_are_unique_and_sorted(repo):
    assert repo.cities() == sorted(["חיפה", "תל אביב", "רחובות"])


def test_get_by_id(repo):
    assert repo.get(3).name == "Rehovot Tower"
    assert repo.get(999) is None
