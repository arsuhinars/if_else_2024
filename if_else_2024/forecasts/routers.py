from typing import Annotated

from annotated_types import Ge
from fastapi import APIRouter, Depends, Path, status

from if_else_2024.auth.dependencies import authenticate_user, is_authenticated
from if_else_2024.core.dependencies import DbSessionDep, ForecastServiceDep
from if_else_2024.forecasts.dto import CreateForecastDto, ForecastDto, UpdateForecastDto

router = APIRouter(prefix="/region/weather/forecast", tags=["Прогнозы погоды"])


@router.get(
    "/{id}",
    summary="Получить прогноз погоды по id",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Прогноза погоды с указанным id не существует"
        }
    },
    dependencies=[Depends(authenticate_user)],
)
async def get_forecast_by_id(
    session: DbSessionDep,
    service: ForecastServiceDep,
    id: Annotated[int, Ge(1), Path()],
) -> ForecastDto:
    forecast = await service.get_by_id(session, id)
    return ForecastDto.model_validate(forecast)


@router.post(
    "",
    summary="Создать новый прогноз погоды",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Региона с указанным regionId не существует"
        },
    },
    dependencies=[Depends(authenticate_user)],
)
async def create_forecast(
    session: DbSessionDep, service: ForecastServiceDep, dto: CreateForecastDto
) -> ForecastDto:
    forecast = await service.create(session, dto)
    return ForecastDto.model_validate(forecast)


@router.put(
    "/{id}",
    summary="Обновить прогноз погоды по id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Прогноза погоды с указанным id не существует"
        },
    },
    dependencies=[Depends(authenticate_user)],
)
async def update_forecast_by_id(
    session: DbSessionDep,
    service: ForecastServiceDep,
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
    session: DbSessionDep,
    service: ForecastServiceDep,
    id: Annotated[int, Ge(1), Path()],
):
    await service.delete_by_id(session, id)
