from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyCookie

from if_else_2024.auth.models import AuthSession
from if_else_2024.core.dependencies import AuthServiceDep, DbSessionDep
from if_else_2024.core.exceptions import UnauthorizedException

session_id_scheme = APIKeyCookie(
    name="id",
    auto_error=False,
    scheme_name="Session id",
    description=(
        "Авторизация по id сессии через cookie. id представлен в виде "
        "уникального UUID"
    ),
)
SessionToken = Annotated[str | None, Depends(session_id_scheme)]


async def authenticate_user(
    auth_service: AuthServiceDep,
    session: DbSessionDep,
    raw_id: SessionToken = None,
):
    if raw_id is None:
        return None

    try:
        id = UUID(raw_id)
    except ValueError:
        raise UnauthorizedException("Invalid session id")

    return await auth_service.validate_session(session, id)


async def is_authenticated(
    auth_session: Annotated[AuthSession | None, Depends(authenticate_user)]
):
    if auth_session is None:
        raise UnauthorizedException("Authentication is required")


AuthSessionDep = Annotated[AuthSession | None, Depends(authenticate_user)]
