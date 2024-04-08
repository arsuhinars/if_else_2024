from fastapi import APIRouter

router = APIRouter(prefix="/accounts", tags=["Аккаунты"])


@router.get(
    "/{id}",
    summary="Получить данные аккаунта по id",
)
def get_account_by_id(id: int):
    pass
