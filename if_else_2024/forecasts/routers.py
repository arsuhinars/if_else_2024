from typing import Annotated

from annotated_types import Ge
from fastapi import APIRouter, Depends, Path, status

from if_else_2024.auth.dependencies import is_authenticated
from if_else_2024.core.dependencies import DbSessionDep
from if_else_2024.forecasts.dto import CreateForecastDto, ForecastDto, UpdateForecastDto
from if_else_2024.forecasts.services import ForecastService

router = APIRouter(prefix="/region/weather/forecast")


@router.get(
    "/{id}",
    summary="Получить прогноз погоды по id",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Прогноза погоды с указанным id не существует"
        }
    },
)
async def get_forecast_by_id(
    session: DbSessionDep, service: ForecastService, id: Annotated[int, Ge(1), Path()]
) -> ForecastDto:
    forecast = await service.get_by_id(session, id)
    return ForecastDto.model_validate(forecast)


@router.post(
    "",
    summary="Создать новый прогноз погоды",
    dependencies=[
        Depends(is_authenticated),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Региона с указанным regionId не существует"
        },
    },
)
async def create_forecast(
    session: DbSessionDep, service: ForecastService, dto: CreateForecastDto
) -> ForecastDto:
    forecast = await service.create(session, dto)
    return ForecastDto.model_validate(forecast)


@router.put(
    "/{id}",
    summary="Обновить прогноз погоды по id",
    dependencies=[Depends(is_authenticated)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Прогноза погоды с указанным id не существует"
        },
    },
)
async def update_forecast_by_id(
    session: DbSessionDep,
    service: ForecastService,
    id: Annotated[int, Ge(1), Path()],
    dto: UpdateForecastDto,
) -> ForecastDto:
    forecast = await service.update_by_id(session, id, dto)
    return ForecastDto.model_validate(forecast)


@router.delete(
    "/{id}",
    summary="Удалить прогноз погоды по id",
    dependencies=[Depends(is_authenticated)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Прогноза погоды с указанным id не существует"
        },
    },
)
async def delete_forecast_by_id(
    session: DbSessionDep, service: ForecastService, id: Annotated[int, Ge(1), Path()]
):
    await service.delete_by_id(session, id)
