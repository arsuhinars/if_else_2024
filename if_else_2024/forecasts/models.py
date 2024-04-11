# flake8: noqa: F821
from datetime import datetime
from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from if_else_2024.core.db_manager import Base


class WeatherCondition(StrEnum):
    CLEAR = "CLEAR"
    CLOUDY = "CLOUDY"
    RAIN = "RAIN"
    SNOW = "SNOW"
    FOG = "FOG"
    STORM = "STORM"


class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime]
    temperature: Mapped[float]
    weather_condition: Mapped[WeatherCondition]
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))

    region: Mapped["Region"] = relationship(back_populates="forecasts")
