from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from if_else_2024.utils import NonEmptyStr


class RegisterAccountDto(BaseModel):
    first_name: Annotated[str, Field(alias="firstName"), NonEmptyStr]
    last_name: Annotated[str, Field(alias="lastName"), NonEmptyStr]
    email: EmailStr
    password: Annotated[str, NonEmptyStr]


class LoginDto(BaseModel):
    email: EmailStr
    password: Annotated[str, NonEmptyStr]


class LoginResponseDto(BaseModel):
    id: int
