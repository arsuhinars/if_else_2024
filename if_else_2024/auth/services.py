from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.accounts.models import Account
from if_else_2024.accounts.repositories import AccountRepository
from if_else_2024.auth.dto import LoginDto, RegisterAccountDto
from if_else_2024.auth.models import AuthSession
from if_else_2024.auth.repositories import AuthRepository
from if_else_2024.auth.utils import pass_context
from if_else_2024.core.exceptions import (
    EntityAlreadyExistsException,
    UnauthorizedException,
)


class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        account_repository: AccountRepository,
        auth_session_lifetime: int,
    ):
        self._auth_repository = auth_repository
        self._account_repository = account_repository
        self._auth_session_lifetime = auth_session_lifetime

    async def register(self, session: AsyncSession, dto: RegisterAccountDto):
        if await self._account_repository.exists_by_email(session, dto.email):
            raise EntityAlreadyExistsException(
                "Account with given email already exists"
            )

        account = Account(**dto.model_dump(exclude=["password"]))
        account.password_hash = pass_context.hash(dto.password)
        session.add(account)
        await session.flush()

        auth_session = AuthSession(account_id=account.id, account=account)
        account.auth_session = auth_session
        session.add(auth_session)
        await session.flush()

        await session.commit()

        return auth_session

    async def login(self, session: AsyncSession, dto: LoginDto):
        account = await self._account_repository.get_by_email(session, dto.email)
        if account is None or not pass_context.verify(
            dto.password, account.password_hash
        ):
            raise UnauthorizedException("Invalid credentials")

        auth_session = await account.awaitable_attrs.auth_session

        if auth_session is not None:
            await session.delete(auth_session)
            await session.flush()

        auth_session = AuthSession(account_id=account.id, account=account)
        account.auth_session = auth_session
        session.add(auth_session)
        await session.flush()

        await session.commit()

        return auth_session

    async def validate_session(self, session: AsyncSession, id: UUID):
        auth_session = await self._auth_repository.get_by_id(session, id)
        if auth_session is None:
            raise UnauthorizedException("Invalid session id")

        if (
            datetime.now() - auth_session.create_date
        ).seconds > self._auth_session_lifetime:
            raise UnauthorizedException("Session is outdated")

        return auth_session
