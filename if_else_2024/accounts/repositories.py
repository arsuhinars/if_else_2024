from sqlalchemy import and_, exists, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.accounts.models import Account


class AccountRepository:
    async def get_by_id(self, session: AsyncSession, id: int):
        return await session.get(Account, id)

    async def get_by_email(self, session: AsyncSession, email: str):
        q = select(Account).where(Account.email == email)
        s = await session.execute(q)
        return s.scalar_one_or_none()

    async def exists_by_email(self, session: AsyncSession, email: str):
        q = select(exists().where(Account.email == email))
        s = await session.execute(q)
        return s.scalar_one()

    async def search(
        self,
        session: AsyncSession,
        first_name: str | None,
        last_name: str | None,
        email: str | None,
        offset: int,
        size: int,
    ):
        conditions = [true()]
        if first_name is not None:
            conditions.append(Account.first_name.icontains(first_name))

        if last_name is not None:
            conditions.append(Account.last_name.icontains(last_name))

        if email is not None:
            conditions.append(Account.email.icontains(email))

        q = (
            select(Account)
            .where(and_(*conditions))
            .order_by(Account.id)
            .offset(offset)
            .limit(size)
        )
        s = await session.execute(q)
        return s.scalars().all()

    async def save(self, session: AsyncSession, account: Account):
        session.add(account)
        await session.flush()
        await session.commit()
        return account

    async def delete(self, session: AsyncSession, account: Account):
        await session.delete(account)
        await session.commit()
