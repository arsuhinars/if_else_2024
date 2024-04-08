# flake8: noqa: F821
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from if_else_2024.core.db_manager import Base


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship(
        back_populates="auth_session", single_parent=True
    )
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())

    # TODO: index for account_id
    __table_args__ = (UniqueConstraint("account_id"),)
