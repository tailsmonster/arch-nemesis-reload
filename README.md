# Arch Nemesis: Reload

Arch Nemesis: Reload is a stateful, LLM-first persuasion game where the player tries to convince an arrogant Arch Linux zealot AI to install Windows.

Current milestone: backend first. React/frontend work is deferred until the backend game loop, LLM path, LangGraph orchestration, persistence, graph inspection page, tests, and eval harness are working.


```mermaid
flowchart TD
    subgraph Client[Client / Future Frontend]
        client_chat_ui["Client Chat UI"]
        client_render_state["Client Renders State"]
        await_next_player_turn["Await Next Player Turn"]
    end
    subgraph API[FastAPI Game API]
        api_create_or_select_game["Create / Select Game"]
        api_select_round_id["Select Round / Turn ID"]
        api_submit_player_argument["Submit Player Argument"]
        api_return_updated_state["Return Updated State"]
    end
    subgraph DB[SQLite Canonical State]
        db_load_game_context["DB Load Context"]
    end
    subgraph LG[LangGraph Executable Turn Workflow]
        graph_turn_start["LangGraph Turn Start"]
        load_context["Load Context"]
        llm_fact_check["llm_fact_check"]
        llm_director_evaluate["llm_director_evaluate"]
        apply_rules["Apply Rules"]
        llm_nemesis_respond["llm_nemesis_respond"]
        persist_turn["Persist Turn"]
    end
    client_chat_ui -->|start/load| api_create_or_select_game
    api_create_or_select_game -->|selected game| api_select_round_id
    api_select_round_id -->|game_id + optional turn_id| db_load_game_context
    db_load_game_context -->|context| api_submit_player_argument
    api_submit_player_argument -->|invoke graph| graph_turn_start
    graph_turn_start -->|TurnGraphState| load_context
    load_context -->|next| llm_fact_check
    llm_fact_check -->|next| llm_director_evaluate
    llm_director_evaluate -->|next| apply_rules
    apply_rules -->|next| llm_nemesis_respond
    llm_nemesis_respond -->|next| persist_turn
    persist_turn -->|saved canonical state| api_return_updated_state
    api_return_updated_state -->|JSON response| client_render_state
    client_render_state -->|display| await_next_player_turn
    await_next_player_turn -->|next turn / inspect round| api_select_round_id
    classDef llm fill:#ffe8cc,stroke:#f08c00,stroke-width:2px;
    classDef db fill:#d3f9d8,stroke:#2f9e44,stroke-width:2px;
    classDef api fill:#d0ebff,stroke:#1c7ed6,stroke-width:2px;
    class llm_fact_check,llm_director_evaluate,llm_nemesis_respond llm;
    class db_load_game_context,persist_turn db;
    class api_create_or_select_game,api_select_round_id,api_submit_player_argument,api_return_updated_state api;
```

## Backend stack

- FastAPI
- LangGraph
- SQLite
- Micromamba
- Real LLM calls by default
- Explicit dry-run mode for tests, CI, offline checks, and reproducible evals

## Run the backend

```bash
cp .env.example .env
cd backend
micromamba env create -f environment.yml
micromamba activate arch-nemesis-reload-backend
python -m pip install -e .
uvicorn arch_nemesis.main:app --reload
```

After the editable install has been run once, normal development startup is:

```bash
cd backend
micromamba activate arch-nemesis-reload-backend
uvicorn arch_nemesis.main:app --reload
```

If shell activation is not initialized for micromamba, use:

```bash
cd backend
micromamba run -n arch-nemesis-reload-backend uvicorn arch_nemesis.main:app --reload
```

The backend runs at `http://localhost:8000`.

## Key URLs

- `GET /api/health`: app/database health
- `GET /api/health/llm`: LLM configuration health
- `POST /api/games`: create a game
- `GET /api/games`: list games
- `GET /api/games/{game_id}`: load a game with messages
- `POST /api/games/{game_id}/turns`: submit a player argument
- `POST /api/llm/respond`: direct Nemesis development endpoint
- `POST /api/llm/fact-check`: direct fact checker development endpoint
- `POST /api/llm/director-evaluate`: direct director development endpoint
- `GET /graph`: browser-viewable LangGraph inspection page
- `GET /api/graph/spec`: JSON graph spec
- `GET /api/graph/mermaid`: Mermaid graph source

## Scripts

```bash
./scripts/dev-backend.sh
./scripts/test-backend.sh
./scripts/run-evals.sh
```

## LLM mode

Real LLM behavior is the primary product path. Set `OPENAI_API_KEY` in `.env` for live OpenAI calls.

Set `DRY_RUN_MODE=true` only for tests, CI, offline development, or deterministic eval harness runs.
