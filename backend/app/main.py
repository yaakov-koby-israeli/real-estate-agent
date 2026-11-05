from fastapi import FastAPI

from app.api import chat_routes, project_routes

app = FastAPI(title="Prashkovsky Real-Estate Agent")
app.include_router(project_routes.router)
app.include_router(chat_routes.router)
