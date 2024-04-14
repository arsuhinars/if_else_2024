from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.forecasts.models import Forecast


class ForecastRepository:
    async def get_by_id(self, session: AsyncSession, id: int):
        return await session.get(Forecast, id)

    async def get_by_region_and_id(
        self, session: AsyncSession, region_id: int, id: int
    ):
        q = select(Forecast).where(
            (Forecast.id == id) & (Forecast.region_id == region_id)
        )
        s = await session.execute(q)
        return s.scalar_one_or_none()

    async def save(self, session: AsyncSession, forecast: Forecast):
        session.add(forecast)
        await session.flush()
        await session.commit()
        return forecast

    async def delete(self, session: AsyncSession, forecast: Forecast):
        await session.delete(forecast)
        await session.commit()
