# flake8: noqa: F821
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from if_else_2024.core.db_manager import Base
from if_else_2024.weather.models import WeatherCondition, weather_forecast_table


class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime]
    temperature: Mapped[float]
    weather_condition: Mapped[WeatherCondition]
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))

    region: Mapped["Region"] = relationship(back_populates="forecasts")
    weather: Mapped[list["Weather"]] = relationship(
        back_populates="forecasts",
        secondary=weather_forecast_table,
        cascade="save-update, merge, delete",
    )
