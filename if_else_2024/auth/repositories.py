from uuid import UUID

from sqlalchemy import exists
from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.auth.models import AuthSession


class AuthRepository:
    async def get_by_id(self, session: AsyncSession, id: UUID):
        return await session.get(AuthSession, id)

    async def exists_by_id(self, session: AsyncSession, id: UUID) -> bool:
        q = exists().where(AuthSession.id == id)
        s = await session.execute(q)
        return s.scalar()
