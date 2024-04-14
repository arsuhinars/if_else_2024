from datetime import datetime

from sqlalchemy import and_, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.weather.models import Weather, WeatherCondition


class WeatherRepository:
    async def get_by_id(self, session: AsyncSession, id: int):
        return await session.get(Weather, id)

    async def search(
        self,
        session: AsyncSession,
        start_date_time: datetime | None,
        end_date_time: datetime | None,
        region_id: int | None,
        weather_condition: WeatherCondition | None,
        offset: int,
        size: int,
    ):
        conditions = [true()]

        if start_date_time is not None:
            conditions.append(Weather.measurement_date_time >= start_date_time)

        if end_date_time is not None:
            conditions.append(Weather.measurement_date_time <= end_date_time)

        if region_id is not None:
            conditions.append(Weather.region_id == region_id)

        if weather_condition is not None:
            conditions.append(Weather.weather_condition == weather_condition)

        q = (
            select(Weather)
            .where(and_(*conditions))
            .order_by(Weather.id)
            .offset(offset)
            .limit(size)
        )
        s = await session.execute(q)

        return s.scalars().all()

    async def save(self, session: AsyncSession, weather: Weather):
        session.add(weather)
        await session.flush()
        await session.commit()
        return weather

    async def delete(self, session: AsyncSession, weather: Weather):
        await session.delete(weather)
        await session.commit()
