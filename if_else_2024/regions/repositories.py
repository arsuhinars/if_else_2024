from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.regions.models import Region, RegionType


class RegionTypeRepository:
    async def get_by_id(self, session: AsyncSession, id: int):
        return await session.get(RegionType, id)

    async def exists_by_type(self, session: AsyncSession, type: str):
        q = select(exists().where(RegionType.type == type))
        s = await session.execute(q)
        return s.scalar_one()

    async def save(self, session: AsyncSession, region_type: RegionType):
        session.add(region_type)
        await session.flush()
        await session.commit()
        return region_type

    async def delete(self, session: AsyncSession, region_type: RegionType):
        await session.delete(region_type)
        await session.commit()


class RegionRepository:
    async def get_by_id(self, session: AsyncSession, id: int):
        return await session.get(Region, id)

    async def get_by_name(self, session: AsyncSession, name: str):
        q = select(Region).where(Region.name == name)
        s = await session.execute(q)
        return s.scalar_one_or_none()

    async def exists_by_name(self, session: AsyncSession, name: str):
        q = select(exists().where(Region.name == name))
        s = await session.execute(q)
        return s.scalar_one()

    async def exists_by_type_id(self, session: AsyncSession, region_type_id: int):
        q = select(exists().where(Region.region_type_id == region_type_id))
        s = await session.execute(q)
        return s.scalar_one()

    async def exists_by_parent_id(self, session: AsyncSession, parent_id: int):
        q = select(exists().where(Region.parent_region_id == parent_id))
        s = await session.execute(q)
        return s.scalar_one()

    async def exists_by_account_id(self, session: AsyncSession, account_id: int):
        q = select(exists().where(Region.account_id == account_id))
        s = await session.execute(q)
        return s.scalar_one()

    async def exists_by_location(
        self, session: AsyncSession, latitude: float, longitude: float
    ):
        q = select(
            exists().where(Region.latitude == latitude & Region.longitude == longitude)
        )
        s = await session.execute(q)
        return s.scalar_one()

    async def save(self, session: AsyncSession, region: Region):
        session.add(region)
        await session.flush()
        await session.commit()
        return region

    async def delete(self, session: AsyncSession, region: Region):
        await session.delete(region)
        await session.commit()
