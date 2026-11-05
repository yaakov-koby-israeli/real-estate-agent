from pydantic import BaseModel

from app.models.enums import ProjectCategory, ProjectFeature, ProjectStatus


class Project(BaseModel):
    id: int
    name: str
    city: str | None = None
    categories: list[ProjectCategory]
    status: ProjectStatus | None = None
    rooms: list[int] = []
    features: list[ProjectFeature] = []
    description: str = ""
    url: str
    image_url: str | None = None
