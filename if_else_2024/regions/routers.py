from typing import Annotated

from annotated_types import Ge
from fastapi import APIRouter, Depends, Path, status

from if_else_2024.auth.dependencies import AuthSessionDep, is_authenticated
from if_else_2024.core.dependencies import (
    DbSessionDep,
    RegionServiceDep,
    RegionTypeServiceDep,
)
from if_else_2024.regions.dto import (
    CreateRegionDto,
    CreateRegionTypeDto,
    RegionDto,
    RegionTypeDto,
    UpdateRegionDto,
    UpdateRegionTypeDto,
)

regions_router = APIRouter(prefix="/", tags=["Регионы"])


@regions_router.get(
    "/{id}",
    summary="Получить данные региона по id",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Региона с указанным id не существует"
        }
    },
)
async def get_region_by_id(
    session: DbSessionDep, service: RegionServiceDep, id: Annotated[int, Ge(1), Path()]
) -> RegionDto:
    region = await service.get_by_id(session, id)
    return RegionDto.model_validate(region)


@regions_router.post(
    summary="Создать новый регион",
    description=(
        "В качестве аккаунта, заполнившего регион, будет выбран текущий, "
        "с которого был выполнен метод\n\n"
        "_Отличия от задания:_\n"
        "Добавлены коды ошибок при несуществовании указанного типа региона или "
        "родителя.\n\n"
        "Также имя региона должно быть уникальным для того, чтобы можно было "
        "однозначно определить родительский регион по имени.\n\n"
        "Добавлены доп. проверки на валидность данных (400 код ошибки):\n"
        "- regionType >= 1\n"
        "- parentRegion не пустая строка"
    ),
    dependencies=[Depends(is_authenticated)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_404_CONFLICT: {
            "description": (
                "Типа региона с `id` равным `regionType` не существует\n"
                "Родительский регион с именем `parentRegion` не существует"
            )
        },
        status.HTTP_409_CONFLICT: {
            "description": (
                "Регион с указанными `latitude` и `longitude` уже существует\n"
                "Регион с указанным именем уже существует"
            )
        },
    },
)
async def create_region(
    session: DbSessionDep,
    service: RegionServiceDep,
    auth: AuthSessionDep,
    dto: CreateRegionDto,
) -> RegionDto:
    region = await service.create(session, auth.account_id, dto)
    return RegionDto.model_validate(region)


@regions_router.put(
    "/{id}",
    summary="Обновить регион по id",
    description="_Отличия от задания:_\nсм. описание метода `POST /region`",
    dependencies=[Depends(is_authenticated)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_404_CONFLICT: {
            "description": (
                "Типа региона с `id` равным `regionType` не существует\n"
                "Родительский регион с именем `parentRegion` не существует"
            )
        },
        status.HTTP_409_CONFLICT: {
            "description": (
                "Регион с указанными `latitude` и `longitude` уже существует\n"
                "Регион с указанным именем уже существует"
            )
        },
    },
)
async def update_region_by_id(
    session: DbSessionDep,
    service: RegionServiceDep,
    auth: AuthSessionDep,
    dto: UpdateRegionDto,
    id: Annotated[int, Ge(1), Path()],
) -> RegionDto:
    region = await service.update_by_id(session, id, auth.account_id, dto)
    return await RegionDto.model_validate(region)


@regions_router.delete(
    "/{id}",
    summary="Удалить регион по id",
    dependencies=[Depends(is_authenticated)],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Регион является родителем другого региона"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
    },
)
async def delete_region_by_id(
    session: DbSessionDep, service: RegionServiceDep, id: Annotated[int, Ge(1), Path()]
):
    await service.delete_by_id(session, id)


regions_types_router = APIRouter(prefix="/types", tags=["Типы регионов"])


@regions_router.get(
    "/{id}",
    summary="Получить тип региона по id",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Типа региона с указанным id не существует"
        }
    },
)
async def get_region_type_by_id(
    session: DbSessionDep, service: RegionTypeServiceDep, id: int
) -> RegionTypeDto:
    region_type = await service.get_by_id(session, id)
    return RegionTypeDto.model_validate(region_type)


@regions_router.post(
    summary="Создать новый тип региона",
    dependencies=[Depends(is_authenticated)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Тип региона с указанным type уже существует"
        },
    },
)
async def create_region_type(
    session: DbSessionDep, service: RegionTypeServiceDep, dto: CreateRegionTypeDto
) -> RegionTypeDto:
    region_type = await service.create(session, dto)
    return RegionTypeDto.model_validate(region_type)


@regions_router.put(
    "/{id}",
    summary="Обновить тип региона по id",
    dependencies=[Depends(is_authenticated)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Типа региона с указанным id не существует"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Тип региона с указанным type уже существует"
        },
    },
)
async def update_region_type_by_id(
    session: DbSessionDep,
    service: RegionTypeServiceDep,
    id: Annotated[int, Ge(1), Path()],
    dto: UpdateRegionTypeDto,
) -> RegionTypeDto:
    region_type = await service.update_by_id(session, id, dto)
    return RegionTypeDto.model_validate(region_type)


@regions_router.delete(
    "/{id}",
    summary="Удалить тип региона по id",
    description=(
        "_Отличия от задания:_\n"
        "Добавлен код ошибки 400, если данный тип используется регионами"
    ),
    dependencies=[Depends(is_authenticated)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_400_CONFLICT: {
            "description": "Существуют регионы, которые используют данный"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Типа региона с указанным id не существует"
        },
    },
)
async def delete_region_type_by_id(
    session: DbSessionDep,
    service: RegionTypeServiceDep,
    id: Annotated[int, Ge(1), Path()],
):
    await service.delete_by_id(session, id)


router = APIRouter(prefix="/region")
router.include_router(regions_router)
router.include_router(regions_types_router)
