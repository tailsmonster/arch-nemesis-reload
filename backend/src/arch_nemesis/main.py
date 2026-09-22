from fastapi import FastAPI

from arch_nemesis.api.router import api_router
from arch_nemesis.api.routes.graph import graph_page_router
from arch_nemesis.database.migrations import initialize_database


def create_app() -> FastAPI:
    app = FastAPI(title="Arch Nemesis: Reload API", version="0.1.0")

    @app.on_event("startup")
    def on_startup() -> None:
        initialize_database()

    app.include_router(api_router, prefix="/api")
    app.include_router(graph_page_router)
    return app


app = create_app()
