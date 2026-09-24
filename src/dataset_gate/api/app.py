"""Application factory; report history location is explicit and test-isolated."""

import importlib
import pkgutil
import sqlite3

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from dataset_gate import __version__
from dataset_gate.api import routes
from dataset_gate.errors import GateError
from dataset_gate.history.store import Store


def create_app(db_path=".dataset-gate/history.db"):
    app = FastAPI(
        title="Dataset Gate",
        version=__version__,
        description="Local data-contract validation. Quality failures return HTTP 200 with a failed report; malformed requests return 4xx.",
    )
    app.state.store = Store(db_path)

    @app.get("/health", tags=["System"])
    def health():
        return {"status": "ok", "version": __version__}

    @app.exception_handler(GateError)
    async def input_error(request: Request, exc: GateError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(sqlite3.Error)
    async def storage_error(request: Request, exc: sqlite3.Error):
        return JSONResponse(
            status_code=503, content={"detail": "History storage is temporarily unavailable"}
        )

    for item in pkgutil.iter_modules(routes.__path__):
        if not item.name.startswith("_"):
            app.include_router(
                importlib.import_module(f"dataset_gate.api.routes.{item.name}").router,
                prefix="/api/v1",
            )
    return app
