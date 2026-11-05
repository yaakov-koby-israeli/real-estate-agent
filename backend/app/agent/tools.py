import json

from app.models.enums import ProjectCategory, ProjectFeature
from app.models.project import Project
from app.services.project_repository import ProjectRepository

MAX_RESULTS = 8
MAX_DESCRIPTION_CHARS = 700


class ProjectTools:
    """The tools the AI agent may ask us to run, and the code that runs them."""

    def __init__(self, repo: ProjectRepository):
        self._repo = repo

    def definitions(self) -> list[dict]:
        """Tool schema in OpenAI's format. City is an enum so the model can only use names we know."""
        return [{
            "type": "function",
            "function": {
                "name": "search_projects",
                "description": (
                    "Search Prashkovsky projects. All filters are optional and combined with AND. "
                    "If there are no results, search again with fewer filters to find alternatives."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "enum": [c.value for c in ProjectCategory]},
                        "city": {"type": "string", "enum": self._repo.cities()},
                        "rooms": {"type": "integer", "minimum": 1, "maximum": 7},
                        "features": {
                            "type": "array",
                            "items": {"type": "string", "enum": [f.value for f in ProjectFeature]},
                        },
                    },
                },
            },
        }]

    def run(self, name: str, arguments_json: str) -> str:
        """Run a tool the model asked for. Always returns JSON text - errors go back to the model, not up."""
        if name != "search_projects":
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            args = json.loads(arguments_json or "{}")
            results = self._repo.search(
                category=ProjectCategory(args["category"]) if args.get("category") else None,
                city=args.get("city"),
                rooms=args.get("rooms"),
                features=[ProjectFeature(f) for f in args.get("features", [])],
            )
        except (ValueError, TypeError) as error:
            return json.dumps({"error": str(error)})
        return json.dumps(
            {"count": len(results), "projects": [summarize(p) for p in results[:MAX_RESULTS]]},
            ensure_ascii=False,
        )


def summarize(project: Project) -> dict:
    return {
        "id": project.id,
        "name": project.name,
        "city": project.city,
        "categories": project.categories,
        "status": project.status,
        "rooms": project.rooms,
        "features": project.features,
        "description": project.description[:MAX_DESCRIPTION_CHARS],
        "url": project.url,
    }
