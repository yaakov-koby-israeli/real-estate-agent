from fastapi import FastAPI

from app.api import project_routes

app = FastAPI(title="Prashkovsky Real-Estate Agent")
app.include_router(project_routes.router)
