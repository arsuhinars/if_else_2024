from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from if_else_2024.utils import NonEmptyStr


class AccountDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: Annotated[str, Field(alias="firstName")]
    last_name: Annotated[str, Field(alias="lastName")]
    email: str


class UpdateAccountDto(BaseModel):
    first_name: Annotated[str, Field(alias="firstName"), NonEmptyStr]
    last_name: Annotated[str, Field(alias="lastName"), NonEmptyStr]
    email: EmailStr
    password: Annotated[str, NonEmptyStr]
