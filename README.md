# Arch Nemesis: Reload
Convince an AI Arch Linux zealot to install Windows. A stateful agentic persuasion game built with LangGraph.

## First vertical slice

- React + TypeScript frontend for starting a game, submitting arguments, and showing chat-style turn history.
- FastAPI backend with SQLite persistence.
- LangGraph turn workflow with separate Nemesis and Judge nodes.
- `DRY_RUN_MODE=true` defaults to deterministic mock LLM behavior for local development and tests.
- Deterministic Python rules own authoritative game-state transitions.

## Backend

The backend app is a FastAPI service. Run it with `uvicorn`, which serves the FastAPI app defined in `app.main:app`.

Backend configuration lives in `backend/.env`. Start from the committed example:

```bash
cd backend
cp .env.example .env
```

For the first vertical slice, keep `DRY_RUN_MODE=true` in `.env` so Nemesis and Judge behavior is deterministic while still flowing through LangGraph.

Micromamba setup:

```bash
cd backend
micromamba env create -f environment.yml
micromamba activate arch-nemesis-reload-backend
uvicorn app.main:app --reload
```

Plain venv setup:

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Run tests:

```bash
cd backend
pytest
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000` unless `VITE_API_BASE` is set.
