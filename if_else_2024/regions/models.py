# flake8: noqa: F821
from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from if_else_2024.core.db_manager import Base


class RegionType(Base):
    __tablename__ = "regions_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]

    regions: Mapped[list["Region"]] = relationship(back_populates="region_type")

    # TODO: add indexes
    __table_args__ = (UniqueConstraint("type"),)


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    region_type_id: Mapped[int] = mapped_column(ForeignKey("regions_types.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    name: Mapped[str]
    parent_region_id: Mapped[int | None] = mapped_column(ForeignKey("regions.id"))
    latitude: Mapped[float]
    longitude: Mapped[float]

    region_type: Mapped[RegionType] = relationship(back_populates="regions")
    account: Mapped["Account"] = relationship(back_populates="regions")
    parent_region: Mapped[Optional["Region"]] = relationship()

    # TODO: add indexes
    __table_args__ = (
        UniqueConstraint("name"),
        UniqueConstraint("latitude", "longitude"),
    )
