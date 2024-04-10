import logging
import sys
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# isort: off
from if_else_2024.core.db_manager import DatabaseManager

# isort: on

from if_else_2024.accounts.repositories import AccountRepository
from if_else_2024.accounts.routers import router as accounts_router
from if_else_2024.accounts.services import AccountService
from if_else_2024.auth.dependencies import authenticate_user
from if_else_2024.auth.repositories import AuthRepository
from if_else_2024.auth.routers import router as auth_router
from if_else_2024.auth.services import AuthService
from if_else_2024.core.exceptions import (
    AppException,
    handle_app_exception,
    handle_validation_exception,
)
from if_else_2024.core.settings import AppSettings
from if_else_2024.core.utils import FakeAccountsCreator
from if_else_2024.regions.repositories import RegionRepository, RegionTypeRepository
from if_else_2024.regions.services import RegionService, RegionTypeService


def create_app() -> FastAPI:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    settings = AppSettings()

    app = FastAPI(
        title="История погоды",
        lifespan=_app_lifespan,
        servers=[
            {"url": settings.server_url, "description": "Локальный сервер"},
        ],
        dependencies=[Depends(authenticate_user)],
        responses={
            400: {"description": "Неверный формат входных данных"},
        },
    )

    """ Setup global dependencies """
    app.state.settings = settings
    app.state.database_manager = DatabaseManager(settings.db_url)
    _setup_app_dependencies(app)

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

    """ Setup exception handlers """
    app.add_exception_handler(AppException, handle_app_exception)
    app.add_exception_handler(RequestValidationError, handle_validation_exception)

    return app


def _setup_app_dependencies(app: FastAPI):
    settings: AppSettings = app.state.settings

    account_repository = AccountRepository()
    auth_repository = AuthRepository()
    region_repository = RegionRepository()
    region_type_repository = RegionTypeRepository()

    account_service = AccountService(account_repository, region_repository)
    auth_service = AuthService(
        auth_repository, account_repository, settings.auth_session_lifetime
    )
    region_service = RegionService(
        region_repository, region_type_repository, account_service
    )
    region_type_service = RegionTypeService(region_type_repository, region_repository)

    app.state.account_service = account_service
    app.state.auth_service = auth_service
    app.state.region_service = region_service
    app.state.region_type_service = region_type_service


@asynccontextmanager
async def _app_lifespan(app: FastAPI):
    settings: AppSettings = app.state.settings
    db: DatabaseManager = app.state.database_manager
    fake_accounts_creator = FakeAccountsCreator(settings.fake_accounts_count)

    if settings.create_fake_accounts:
        async with db.create_session() as session:
            await fake_accounts_creator.create(session)

    await db.initialize()
    yield
    await db.dispose()

    if settings.create_fake_accounts:
        async with db.create_session() as session:
            await fake_accounts_creator.release(session)
