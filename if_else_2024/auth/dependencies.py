from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends

from if_else_2024.auth.models import AuthSession
from if_else_2024.core.dependencies import AuthServiceDep, DbSessionDep
from if_else_2024.core.exceptions import UnauthorizedException


async def authenticate_user(
    auth_service: AuthServiceDep,
    session: DbSessionDep,
    raw_id: Annotated[str | None, Cookie()],
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
