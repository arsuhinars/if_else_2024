import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from if_else_2024.accounts.routers import router as accounts_router
from if_else_2024.auth.routers import router as auth_router
from if_else_2024.core.db_manager import DatabaseManager
from if_else_2024.core.settings import AppSettings


def create_app() -> FastAPI:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    settings = AppSettings()

    app = FastAPI(
        title="История погоды",
        lifespan=_app_lifespan,
        servers=[
            {"url": settings.server_url, "description": "Локальный сервер"},
        ],
    )

    """ Setup global dependencies """
    app.state.settings = settings
    app.state.database_manager = DatabaseManager(settings.db_url)

    """ Setup middlewares """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    """ Setup routers """
    app.include_router(auth_router)
    app.include_router(accounts_router)

    return app


@asynccontextmanager
async def _app_lifespan(app: FastAPI):
    db: DatabaseManager = app.state.database_manager

    await db.initialize()

    yield

    await db.dispose()
