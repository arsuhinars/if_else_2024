# flake8: noqa: F821
from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from if_else_2024.core.db_manager import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]

    auth_session: Mapped[Optional["AuthSession"]] = relationship(
        back_populates="account", cascade="save-update, merge, delete"
    )
    regions: Mapped[list["Region"]] = relationship(
        back_populates="account", cascade="save-update, merge, delete"
    )

    # TODO: add indexes
    __table_args__ = (UniqueConstraint("email"),)
