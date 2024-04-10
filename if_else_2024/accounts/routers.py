from typing import Annotated

from annotated_types import Ge
from fastapi import APIRouter, Depends, Path, Query, status

from if_else_2024.accounts.dto import AccountDto, UpdateAccountDto
from if_else_2024.auth.dependencies import AuthSessionDep, is_authenticated
from if_else_2024.core.dependencies import AccountServiceDep, DbSessionDep
from if_else_2024.core.exceptions import ForbiddenException

router = APIRouter(prefix="/accounts", tags=["Аккаунты"])


@router.get(
    "/search",
    summary="Запрос для поиска аккаунтов",
    description=(
        "Параметры `firstName`, `lastName`, `email` используются для фильтрации "
        "по соответствующим полям. Проверка идет без учета регистра и может "
        "использоваться для проверки только части строки от заданного параметра."
        "\n\n"
        "Параметры `from` и `size` позволяют реализовать пагинацию. Первый "
        "параметр отвечает за количество пропущенных элементов от начала. "
        "Второй - за количество элементов на странице"
    ),
)
async def search_accounts(
    session: DbSessionDep,
    service: AccountServiceDep,
    first_name: Annotated[str | None, Query(alias="firstName")] = None,
    last_name: Annotated[str | None, Query(alias="lastName")] = None,
    email: Annotated[str | None, Query()] = None,
    offset: Annotated[int, Query(alias="from"), Ge(0)] = 0,
    size: Annotated[int, Query(), Ge(1)] = 10,
) -> list[AccountDto]:
    accounts = await service.search(session, first_name, last_name, email, offset, size)
    return list(map(AccountDto.model_validate, accounts))


@router.get(
    "/{id}",
    summary="Получить данные аккаунта по id",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Аккаунта с указанным id не существует"
        },
    },
)
async def get_account_by_id(
    session: DbSessionDep, service: AccountServiceDep, id: Annotated[int, Ge(1), Path()]
) -> AccountDto:
    account = await service.get_by_id(session, id)
    return AccountDto.model_validate(account)


@router.put(
    "/{id}",
    summary="Обновить аккаунт по id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Обновление чужого аккаунта или аккаунт не существует"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Аккаунт с таким email уже существует"
        },
    },
    dependencies=[Depends(is_authenticated)],
)
async def update_account_by_id(
    session: DbSessionDep,
    service: AccountServiceDep,
    auth: AuthSessionDep,
    dto: UpdateAccountDto,
    id: Annotated[int, Ge(1), Path()],
) -> AccountDto:
    if id != auth.account_id:
        raise ForbiddenException("You are not allowed to update others accounts")

    account = await service.update_by_id(session, auth.account_id, dto)
    return AccountDto.model_validate(account)


@router.delete(
    "/{id}",
    summary="Удалить аккаунт по id",
    description=(
        "_Отличия от задания:_\n"
        "Добавил ошибку с кодом 400 для того, чтобы избежать нарушения "
        "целостности в БД (поле accountId у региона)"
    ),
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Аккаунт является создателем какого-либо региона"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Запрос от неавторизованного аккаунта"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Обновление чужого аккаунта или аккаунт не существует"
        },
    },
    dependencies=[Depends(is_authenticated)],
)
async def delete_account_by_id(
    session: DbSessionDep,
    service: AccountServiceDep,
    auth: AuthSessionDep,
    id: Annotated[int, Ge(1), Path()],
) -> None:
    if id != auth.account_id:
        raise ForbiddenException("You are not allowed to update others accounts")

    await service.delete_by_id(session, auth.account_id)
