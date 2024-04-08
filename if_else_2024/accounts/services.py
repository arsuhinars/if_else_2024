from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.accounts.dto import UpdateAccountDto
from if_else_2024.accounts.repositories import AccountRepository
from if_else_2024.auth.utils import pass_context
from if_else_2024.core.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)


class AccountService:
    def __init__(self, account_repository: AccountRepository):
        self._repository = account_repository

    async def get_by_id(self, session: AsyncSession, id: int):
        account = await self._repository.get_by_id(session, id)
        if account is None:
            raise EntityNotFoundException("Account with given id was not found")
        return account

    async def search(
        self,
        session: AsyncSession,
        first_name: str | None,
        last_name: str | None,
        email: str | None,
        offset: int,
        size: int,
    ):
        return list(
            await self._repository.search(
                session, first_name, last_name, email, offset, size
            )
        )

    async def update_by_id(self, session: AsyncSession, id: int, dto: UpdateAccountDto):
        account = await self._repository.get_by_id(session, id)
        if account is None:
            raise EntityNotFoundException("Account with given id was not found")

        if dto.email != account.email and await self._repository.exists_by_email(
            session, dto.email
        ):
            raise EntityAlreadyExistsException(
                "Account with given email already exists"
            )

        account.first_name = dto.first_name
        account.last_name = dto.last_name
        account.email = dto.email
        account.password_hash = pass_context.hash(dto.password)

        return await self._repository.save(session, account)

    async def delete_by_id(self, session: AsyncSession, id: int):
        account = await self._repository.get_by_id(session, id)
        if account is None:
            raise EntityNotFoundException("Account with given id was not found")

        await self._repository.delete(session, account)
