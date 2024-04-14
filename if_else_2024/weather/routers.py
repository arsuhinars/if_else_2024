from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query

from if_else_2024.core.dependencies import DbSessionDep, WeatherServiceDep
from if_else_2024.weather.dto import CreateWeatherDto, UpdateWeatherDto, WeatherDto
from if_else_2024.weather.models import WeatherCondition

router = APIRouter(prefix="/region", tags=["Погода"])


@router.get(
    "/weather/{region_id}",
    summary="Получить данные текущей погоды в регионе по region_id",
)
async def get_weather_by_region_id(
    session: DbSessionDep, service: WeatherServiceDep, region_id: int
) -> WeatherDto:
    weather = await service.get_current_for_region(session, region_id)
    return WeatherDto.model_validate(weather)


@router.get(
    "/weather/search",
    summary="Запрос для поиска погоды",
    description=(
        "Параметры `startDateTime` и `endDateTime` задают период начала и конца"
        "соответственно для поиска записей о погоде."
        "\n\n"
        "Параметры `regionId` и `weatherCondition` используются для фильтрации "
        "по соответствующим полям."
        "\n\n"
        "Параметры `from` и `size` позволяют реализовать пагинацию. Первый "
        "параметр отвечает за количество пропущенных элементов от начала. "
        "Второй - за количество элементов на странице"
    ),
)
async def search_weather(
    session: DbSessionDep,
    service: WeatherServiceDep,
    start_date_time: Annotated[datetime | None, Query(alias="startDateTime")] = None,
    end_date_time: Annotated[datetime | None, Query(alias="startDateTime")] = None,
    region_id: Annotated[int | None, Query(alias="regionId")] = None,
    weather_condition: Annotated[
        WeatherCondition | None, Query(alias="weatherCondition")
    ] = None,
    offset: Annotated[int, Query(alias="from")] = 0,
    size: Annotated[int, Query(alias="size")] = 10,
) -> list[WeatherDto]:
    weather = await service.search(
        session,
        start_date_time,
        end_date_time,
        region_id,
        weather_condition,
        offset,
        size,
    )
    return list(map(WeatherDto.model_validate, weather))


@router.post(
    "/weather",
    summary="Создать новую погоду и сделать её текущей для региона по region_id",
)
async def create_weather_for_region(
    session: DbSessionDep,
    service: WeatherServiceDep,
    region_id: int,
    dto: CreateWeatherDto,
) -> WeatherDto:
    weather = await service.create_current_for_region(session, region_id, dto)
    return WeatherDto.model_validate(weather)


@router.put(
    "/weather/{region_id}",
    summary="Обновить текущую погоду для региона по region_id",
)
async def update_weather_for_region(
    session: DbSessionDep,
    service: WeatherServiceDep,
    region_id: int,
    dto: UpdateWeatherDto,
) -> WeatherDto:
    weather = await service.update_current_for_region(session, region_id, dto)
    return WeatherDto.model_validate(weather)


@router.delete(
    "/weather/{region_id}",
    summary="Удалить текущую погоду в регионе по region_id",
)
async def delete_weather_for_region(
    session: DbSessionDep, service: WeatherServiceDep, region_id: int
):
    await service.delete_current_for_region(session, region_id)


@router.post(
    "/{region_id}/weather/{weather_id}",
    summary="Заменить текущую погоду в регионе с region_id на погоду с weather_id",
)
async def set_current_weather_for_region(
    session: DbSessionDep, service: WeatherServiceDep, region_id: int, weather_id: int
):
    await service.set_current_for_region(session, region_id, weather_id)


@router.delete(
    "/{region_id}/weather/{weather_id}",
    summary="Удалить погоду в регионе с region_id по weather_id",
)
async def delete_weather(
    session: DbSessionDep, service: WeatherServiceDep, region_id: int, weather_id: int
):
    await service.delete_by_id(session, region_id, weather_id)
