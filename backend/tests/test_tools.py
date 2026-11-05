import json

import pytest

from app.agent.tools import MAX_DESCRIPTION_CHARS, ProjectTools
from app.services.project_repository import ProjectRepository

TEST_PROJECTS = [
    {"id": 1, "name": "Haifa Park", "city": "חיפה", "categories": ["residential"],
     "features": ["park"], "description": "א" * 2000, "url": "https://example.com/1"},
    {"id": 2, "name": "Tel Aviv Rent", "city": "תל אביב", "categories": ["rental"],
     "url": "https://example.com/2"},
]


@pytest.fixture
def tools(tmp_path):
    projects_file = tmp_path / "projects.json"
    projects_file.write_text(json.dumps(TEST_PROJECTS), encoding="utf-8")
    return ProjectTools(ProjectRepository(projects_file))


def run_search(tools, **args):
    return json.loads(tools.run("search_projects", json.dumps(args)))


def test_city_enum_comes_from_repository(tools):
    city_schema = tools.definitions()[0]["function"]["parameters"]["properties"]["city"]
    assert city_schema["enum"] == sorted(["חיפה", "תל אביב"])


def test_search_filters_results(tools):
    result = run_search(tools, category="rental")
    assert result["count"] == 1
    assert result["projects"][0]["name"] == "Tel Aviv Rent"


def test_empty_arguments_return_everything(tools):
    assert json.loads(tools.run("search_projects", ""))["count"] == 2


def test_description_is_truncated(tools):
    project = run_search(tools, city="חיפה")["projects"][0]
    assert len(project["description"]) == MAX_DESCRIPTION_CHARS


def test_invalid_argument_returns_error_instead_of_crashing(tools):
    assert "error" in run_search(tools, category="castle")


def test_unknown_tool_returns_error(tools):
    assert "error" in json.loads(tools.run("delete_everything", "{}"))
