from sqlalchemy.orm import Mapped, mapped_column

from if_else_2024.core.db_manager import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]

    # TODO: add indexes
