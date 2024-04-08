from fastapi import APIRouter, Response, status

from if_else_2024.accounts.dto import AccountDto
from if_else_2024.auth.dependencies import AuthSessionDep
from if_else_2024.auth.dto import LoginDto, LoginResponseDto, RegisterAccountDto
from if_else_2024.core.dependencies import AuthServiceDep, DbSessionDep
from if_else_2024.core.exceptions import ForbiddenException

router = APIRouter(prefix="", tags=["Аутентификация"])


@router.post(
    "/registration",
    summary="Регистрация нового пользователя",
    description=(
        "После успешной регистрации в cookie параметр `id` будет "
        "записан идентификатор текущей сессии. Для повторного входа в аккаунт "
        "воспользуйтесь методом `/login`"
    ),
    status_code=status.HTTP_201_CREATED,
)
async def register(
    dto: RegisterAccountDto,
    session: DbSessionDep,
    service: AuthServiceDep,
    auth: AuthSessionDep,
    response: Response,
):
    if auth is not None:
        raise ForbiddenException("You are already authorized")

    auth_session = await service.register(session, dto)

    response.set_cookie("id", auth_session.id.hex)

    return AccountDto.model_validate(auth_session.account)


@router.post(
    "/login",
    summary="Вход в существующий аккаунт",
    description=(
        "После успешного входа в cookie параметр `id` будет "
        "записан идентификатор текущей сессии. Сессия активна только некоторое "
        "время, после которого необходимо входить в аккаунт заново."
    ),
)
async def login(
    dto: LoginDto,
    session: DbSessionDep,
    service: AuthServiceDep,
    response: Response,
):
    auth_session = await service.login(session, dto)

    response.set_cookie("id", auth_session.id.hex)

    return LoginResponseDto(id=auth_session.account.id)
