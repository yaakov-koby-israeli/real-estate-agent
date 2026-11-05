import json

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_project_repository
from app.main import app
from app.services.project_repository import ProjectRepository

TEST_PROJECTS = [
    {"id": 1, "name": "Haifa Park", "city": "חיפה", "categories": ["residential"], "url": "https://example.com/1"},
    {"id": 2, "name": "Tel Aviv Rent", "city": "תל אביב", "categories": ["rental"], "url": "https://example.com/2"},
]


@pytest.fixture
def client(tmp_path):
    projects_file = tmp_path / "projects.json"
    projects_file.write_text(json.dumps(TEST_PROJECTS), encoding="utf-8")
    app.dependency_overrides[get_project_repository] = lambda: ProjectRepository(projects_file)
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_search_by_category(client):
    response = client.get("/api/projects", params={"category": "rental"})
    assert response.status_code == 200
    assert [p["id"] for p in response.json()] == [2]


def test_invalid_category_is_rejected(client):
    response = client.get("/api/projects", params={"category": "castle"})
    assert response.status_code == 422


def test_list_cities(client):
    assert client.get("/api/projects/cities").json() == sorted(["חיפה", "תל אביב"])


def test_get_project_not_found(client):
    assert client.get("/api/projects/999").status_code == 404
