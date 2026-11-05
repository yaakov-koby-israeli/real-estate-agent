import json
from pathlib import Path

from app.models.enums import ProjectCategory, ProjectFeature
from app.models.project import Project


class ProjectRepository:
    """The only place that knows where project data is stored."""

    def __init__(self, projects_file: Path):
        data = json.loads(projects_file.read_text(encoding="utf-8"))
        self._projects = [Project.model_validate(item) for item in data]

    def all(self) -> list[Project]:
        return list(self._projects)

    def get(self, project_id: int) -> Project | None:
        return next((p for p in self._projects if p.id == project_id), None)

    def cities(self) -> list[str]:
        return sorted({p.city for p in self._projects if p.city})

    def search(
        self,
        category: ProjectCategory | None = None,
        city: str | None = None,
        rooms: int | None = None,
        features: list[ProjectFeature] | None = None,
    ) -> list[Project]:
        """Return projects matching ALL given filters. A filter left as None is ignored."""
        results = []
        for project in self._projects:
            if category and category not in project.categories:
                continue
            if city and project.city != city:
                continue
            # Unknown rooms (empty list) is not "no match" - the agent will read the description.
            if rooms and project.rooms and rooms not in project.rooms:
                continue
            if features and not all(f in project.features for f in features):
                continue
            results.append(project)
        return results
