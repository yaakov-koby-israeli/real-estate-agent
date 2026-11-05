from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_project_repository
from app.models.enums import ProjectCategory, ProjectFeature
from app.models.project import Project
from app.services.project_repository import ProjectRepository

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("")
def search_projects(
    category: ProjectCategory | None = None,
    city: str | None = None,
    rooms: int | None = None,
    features: list[ProjectFeature] | None = Query(None),
    repo: ProjectRepository = Depends(get_project_repository),
) -> list[Project]:
    return repo.search(category=category, city=city, rooms=rooms, features=features)


@router.get("/cities")
def list_cities(repo: ProjectRepository = Depends(get_project_repository)) -> list[str]:
    return repo.cities()


@router.get("/{project_id}")
def get_project(project_id: int, repo: ProjectRepository = Depends(get_project_repository)) -> Project:
    project = repo.get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
