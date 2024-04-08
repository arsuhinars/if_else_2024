# flake8: noqa: F821
from sqlalchemy import LargeBinary, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from if_else_2024.core.db_manager import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]

    auth_session: Mapped["AuthSession" | None] = relationship(back_populates="account")

    # TODO: add indexes
    __table_args__ = (UniqueConstraint("email"),)
