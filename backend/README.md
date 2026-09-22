# Arch Nemesis: Reload Backend

FastAPI, LangGraph, SQLite, and LLM-first agent services for the backend vertical slice.

## Run

```bash
micromamba env create -f environment.yml
micromamba run -n arch-nemesis-reload-backend uvicorn arch_nemesis.main:app --reload
```

The backend runs at `http://localhost:8000`. APIs live under `/api`; the LangGraph inspection page is `/graph`.
