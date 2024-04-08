from fastapi import APIRouter

router = APIRouter(prefix="/accounts", tags=["Аккаунты"])


# @router.get(
#     "/{id}",
#     summary="Получить данные аккаунта по id",
#     responses={
#         400: "Неверный формат данных",
#         401: "Неверные авторизационные данные",
#         404: "Аккаунт с указанным id не существует",
#     },
# )
# def get_account_by_id(id: int):
#     pass
