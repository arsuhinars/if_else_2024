from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.accounts.services import AccountService
from if_else_2024.auth.services import AuthService
from if_else_2024.core.db_manager import DatabaseManager
from if_else_2024.core.settings import AppSettings
from if_else_2024.forecasts.services import ForecastService
from if_else_2024.regions.services import RegionService, RegionTypeService


def get_settings(request: Request) -> AppSettings:
    return request.app.state.settings


def get_database_manager(request: Request) -> DatabaseManager:
    return request.app.state.database_manager


def get_account_service(request: Request) -> AccountService:
    return request.app.state.account_service


def get_auth_service(request: Request) -> AuthService:
    return request.app.state.auth_service


def get_region_service(request: Request) -> RegionService:
    return request.app.state.region_service


def get_region_type_service(request: Request) -> RegionTypeService:
    return request.app.state.region_type_service


def get_forecast_service(request: Request) -> ForecastService:
    return request.app.state.forecast_service


async def get_db_session(db: Annotated[DatabaseManager, Depends(get_database_manager)]):
    async with db.create_session() as session:
        yield session


SettingsDep = Annotated[AppSettings, Depends(get_settings)]
DatabaseManagerDep = Annotated[DatabaseManager, Depends(get_database_manager)]
AccountServiceDep = Annotated[AccountService, Depends(get_account_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
RegionServiceDep = Annotated[RegionService, Depends(get_region_service)]
RegionTypeServiceDep = Annotated[RegionTypeService, Depends(get_region_type_service)]
ForecastServiceDep = Annotated[ForecastService, Depends(get_forecast_service)]
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
