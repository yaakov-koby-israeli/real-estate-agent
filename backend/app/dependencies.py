from functools import lru_cache

from app.config import PROJECTS_FILE
from app.services.project_repository import ProjectRepository


@lru_cache
def get_project_repository() -> ProjectRepository:
    """Created once on first use, then the same instance is reused for every request."""
    return ProjectRepository(PROJECTS_FILE)
