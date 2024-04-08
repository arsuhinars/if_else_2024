from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.accounts.services import AccountService
from if_else_2024.auth.services import AuthService
from if_else_2024.core.db_manager import DatabaseManager
from if_else_2024.core.settings import AppSettings


def get_settings(request: Request) -> AppSettings:
    return request.app.state.settings


def get_database_manager(request: Request) -> DatabaseManager:
    return request.app.state.database_manager


def get_account_service(request: Request) -> AccountService:
    return request.app.state.account_service


def get_auth_service(request: Request) -> AuthService:
    return request.app.state.auth_service


async def get_db_session(db: Annotated[DatabaseManager, Depends(get_database_manager)]):
    async with db.create_session() as session:
        yield session


SettingsDep = Annotated[AppSettings, Depends(get_settings)]
DatabaseManagerDep = Annotated[DatabaseManager, Depends(get_database_manager)]
AccountServiceDep = Annotated[AccountService, Depends(get_account_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
