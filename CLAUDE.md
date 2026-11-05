# CLAUDE.md

## Project goal
A chat-bot on a copy of the Prashkovsky website that helps visitors find a suitable project
(residential / rental, urban renewal as an alternative). It collects the lead's name and phone,
uses an AI agent to match free-text preferences against our stored project data, and saves a
conversation summary for the sales department.

## Stack
- **Backend:** Python 3.12, FastAPI, Pydantic, OpenAI SDK, requests + BeautifulSoup (scraper)
- **Frontend:** React (Vite)
- **Storage:** JSON files — `backend/data/projects.json`, `backend/data/leads/*.json`

## Structure
```
backend/app/
  models/     Pydantic models + Enums (ProjectCategory, ChatStep)
  scraper/    pulls project data from prashkovsky.co.il
  services/   validation, project_repository, chat_flow, lead_service
  agent/      OpenAI agent + prompts (the ONLY place that calls the LLM for chat)
  api/        FastAPI routes
frontend/src/
  components/site/   site copy
  components/chat/   chat widget
  api/               backend calls
```

## Commands
Run from `backend/`:
```bash
python -m venv .venv                             # once
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m scripts.run_scraper      # refresh data/projects.json from the WordPress API
.venv\Scripts\python -m pytest                   # run tests (use fake data via tmp_path, never the real projects.json)
.venv\Scripts\python -m uvicorn app.main:app --reload   # dev server, API docs at http://127.0.0.1:8000/docs
```

## Backend conventions
- Routes get services through FastAPI `Depends` (see `app/dependencies.py`), so tests can swap them
  with `app.dependency_overrides`.
- Static routes (e.g. `/cities`) must be declared before path-parameter routes (`/{project_id}`).

## Data source
Projects come from the site's WordPress REST API (`/wp-json/wp/v2/project`), not HTML scraping.
`scraper/project_parser.py` maps WordPress category slugs to our enums and extracts city/rooms/features
with simple keyword rules. Tags are a first-pass filter — the full `description` is kept for the agent.

## Local scratch
`scratch/` (git-ignored) holds throwaway exploration scripts and downloads. Keep all temp files there.

## Code rules
- Keep it as simple as possible. Classes and Enums only when they make the code clearer.
- Split files by responsibility — not everything in one file.
- Code, names, and comments in English. User-facing bot text in Hebrew.
- The deterministic flow (type choice, name, phone, callback question) lives in `services/chat_flow.py`
  with no AI. Only free-text preferences go to `agent/`.

## Git policy
- One branch per step: `feature/<step-name>` from `main`.
- Commit every small working unit. Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `test:`.
- Push + merge to `main` at the end of each step, after tests pass and the user approved.
- Never commit broken code, `.env`, API keys, or `backend/data/leads/` (customer personal data).
  The GitHub repo is **public**.

## Way of working (most important)
This project is built as a senior guiding a junior:
- Work in small micro-steps (one file or concept each). Never deliver a whole step at once.
- Before code: explain the concept and why. After code: walk through it and mention common mistakes.
- Run/test each piece, then stop and wait for the user's OK.
- Never commit or push without the user's explicit approval. Explain each git command first.
- Chat with the user in Hebrew; docs and code in English.
