from faker import Faker
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.accounts.models import Account
from if_else_2024.auth.utils import pass_context

# from if_else_2024.regions.models import Region


class FakeDataCreator:
    def __init__(self, accounts_count: int):
        self.__accounts_count = accounts_count
        # self.__regions_count = regions_count
        self.__faker = Faker(locale="ru_RU", use_weighting=False)

    async def create(self, session: AsyncSession):
        q = select(func.count()).select_from(Account)
        accounts_count = (await session.execute(q)).scalar_one()

        # q = select(func.count()).select_from(Region)
        # regions_count = (await session.execute(q)).scalar_one()

        self.__accounts = [
            Account(
                first_name=self.__faker.first_name(),
                last_name=self.__faker.last_name(),
                email=self.__faker.email(),
                password_hash=pass_context.hash(self.__faker.password()),
            )
            for i in range(self.__accounts_count - accounts_count)
        ]
        # self.__regions = []
        # for i in range(self.__regions_count - regions_count):
        #     self.__regions.append(Region(

        #     ))

        session.add_all(self.__accounts)
        await session.flush()
        await session.commit()

    async def release(self, session: AsyncSession):
        # for account in self.__accounts:
        #     await session.delete(account)
        # await session.flush()
        # await session.commit()
        pass
