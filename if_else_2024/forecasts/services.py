from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.core.exceptions import EntityNotFoundException
from if_else_2024.forecasts.dto import CreateForecastDto, UpdateForecastDto
from if_else_2024.forecasts.models import Forecast
from if_else_2024.forecasts.repositories import ForecastRepository
from if_else_2024.regions.repositories import RegionRepository


class ForecastService:
    def __init__(
        self, repository: ForecastRepository, region_repository: RegionRepository
    ):
        self._repository = repository
        self._region_repository = region_repository

    async def create(self, session: AsyncSession, dto: CreateForecastDto):
        region = await self._region_repository.get_by_id(session, dto.region_id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")

        forecast = Forecast(
            **dto.model_dump(exclude=["region_id"]),
            region=region,
        )

        return await self._repository.save(session, forecast)

    async def get_by_id(self, session: AsyncSession, id: int):
        forecast = await self._repository.get_by_id(session, id)
        if forecast is None:
            raise EntityNotFoundException("Forecast with given id was not found")
        return forecast

    async def update_by_id(
        self, session: AsyncSession, id: int, dto: UpdateForecastDto
    ):
        forecast = await self._repository.get_by_id(session, id)
        if forecast is None:
            raise EntityNotFoundException("Forecast with given id was not found")

        forecast.temperature = dto.temperature
        forecast.weather_condition = dto.weather_condition
        forecast.date_time = dto.date_time

        return await self._repository.save(session, forecast)

    async def delete_by_id(self, session: AsyncSession, id: int):
        forecast = await self._repository.get_by_id(session, id)
        if forecast is None:
            raise EntityNotFoundException("Forecast with given id was not found")
        await self._repository.delete(session, forecast)
