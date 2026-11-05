import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).parent.parent
DATA_DIR = BACKEND_DIR / "data"
PROJECTS_FILE = DATA_DIR / "projects.json"

load_dotenv(BACKEND_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
