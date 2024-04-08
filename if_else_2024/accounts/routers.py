from typing import Annotated

from annotated_types import Ge
from fastapi import APIRouter, Path, Query, status

from if_else_2024.accounts.dto import AccountDto
from if_else_2024.core.dependencies import AccountServiceDep, DbSessionDep

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
        }
    },
)
async def get_account_by_id(
    session: DbSessionDep, service: AccountServiceDep, id: Annotated[int, Ge(1), Path()]
) -> AccountDto:
    account = await service.get_by_id(session, id)
    return AccountDto.model_validate(account)
