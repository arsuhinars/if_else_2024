from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from if_else_2024.core.exceptions import EntityNotFoundException
from if_else_2024.forecasts.repositories import ForecastRepository
from if_else_2024.regions.repositories import RegionRepository
from if_else_2024.weather.dto import CreateWeatherDto, UpdateWeatherDto
from if_else_2024.weather.models import Weather, WeatherCondition
from if_else_2024.weather.repositories import WeatherRepository


class WeatherService:
    def __init__(
        self,
        weather_repository: WeatherRepository,
        forecast_repository: ForecastRepository,
        region_repository: RegionRepository,
    ):
        self._weather_repository = weather_repository
        self._forecast_repository = forecast_repository
        self._region_repository = region_repository

    async def create_current_for_region(
        self, session: AsyncSession, region_id: int, dto: CreateWeatherDto
    ):
        region = await self._region_repository.get_by_id(session, region_id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")

        forecasts = [
            await self._forecast_repository.get_by_region_and_id(session, region_id, id)
            for id in dto.weather_forecast
        ]
        if None in forecasts:
            raise EntityNotFoundException(
                "Forecast with one of given ids was not found"
            )

        weather = Weather(
            **dto.model_dump(exclude=["weather_forecast", "region_id"]),
            region=region,
            forecasts=forecasts
        )
        region.current_weather = weather

        session.add(weather)
        session.add(region)
        await session.flush()
        await session.commit()

        return weather

    async def get_current_for_region(self, session: AsyncSession, region_id: int):
        region = await self._region_repository.get_by_id(session, region_id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")

        weather: Weather = await region.awaitable_attrs.current_weather
        if weather is None:
            raise EntityNotFoundException("There is no current weather in this region")

        return weather

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
        return list(
            await self._weather_repository.search(
                session,
                start_date_time,
                end_date_time,
                region_id,
                weather_condition,
                offset,
                size,
            )
        )

    async def update_current_for_region(
        self, session: AsyncSession, region_id: int, dto: UpdateWeatherDto
    ):
        region = await self._region_repository.get_by_id(session, region_id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")

        weather: Weather = await region.awaitable_attrs.current_weather
        if weather is None:
            raise EntityNotFoundException("There is no current weather in this region")

        forecasts = [
            await self._forecast_repository.get_by_region_and_id(session, region_id, id)
            for id in dto.weather_forecast
        ]
        if None in forecasts:
            raise EntityNotFoundException(
                "Forecast with one of given ids was not found"
            )

        region.name = dto.region_name
        weather.temperature = dto.temperature
        weather.humidity = dto.humidity
        weather.wind_speed = dto.wind_speed
        weather.weather_condition = dto.weather_condition
        weather.precipitation_amount = dto.precipitation_amount
        weather.measurement_date_time = dto.measurement_date_time
        weather.forecasts = forecasts

        await session.flush()
        await session.commit()

        return weather

    async def set_current_for_region(
        self, session: AsyncSession, region_id: int, id: int
    ):
        region = await self._region_repository.get_by_id(session, region_id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")

        weather = await self._weather_repository.get_by_id(session, id)
        if weather is None or weather.region_id != region_id:
            raise EntityNotFoundException("There is no current weather in this region")

        region.current_weather = weather
        await self._region_repository.save(session, region)

    async def delete_current_for_region(self, session: AsyncSession, region_id: int):
        region = await self._region_repository.get_by_id(session, region_id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")

        weather: Weather = await region.awaitable_attrs.current_weather
        if weather is None:
            raise EntityNotFoundException("There is no current weather in this region")

        region.current_weather_id = None

        await session.delete(weather)
        await session.flush()
        await session.commit()

    async def delete_by_id(self, session: AsyncSession, region_id: int, id: int):
        region = await self._region_repository.get_by_id(session, region_id)
        if region is None:
            raise EntityNotFoundException("Region with given id was not found")

        weather = await self._weather_repository.get_by_id(session, id)
        if weather is None or weather.region_id != region_id:
            raise EntityNotFoundException(
                "There is no weather with given id in this region"
            )

        if weather.id == region.current_weather_id:
            region.current_weather_id = None

        await session.delete(weather)
        await session.flush()
        await session.commit()
