from fastapi import APIRouter

from arch_nemesis.api.routes import games, graph, health, llm, turns

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(games.router, prefix="/games", tags=["games"])
api_router.include_router(turns.router, prefix="/games", tags=["turns"])
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])
