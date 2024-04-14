# flake8: noqa: F821
from datetime import datetime
from enum import StrEnum

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from if_else_2024.core.db_manager import Base


class WeatherCondition(StrEnum):
    CLEAR = "CLEAR"
    CLOUDY = "CLOUDY"
    RAIN = "RAIN"
    SNOW = "SNOW"
    FOG = "FOG"
    STORM = "STORM"


weather_forecast_table = Table(
    "weather_forecast",
    Base.metadata,
    Column("weather_id", ForeignKey("weather.id"), primary_key=True),
    Column("forecast_id", ForeignKey("forecasts.id"), primary_key=True),
)


class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(primary_key=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    temperature: Mapped[float]
    humidity: Mapped[float]
    wind_speed: Mapped[float]
    weather_condition: Mapped[WeatherCondition]
    precipitation_amount: Mapped[float]
    measurement_date_time: Mapped[datetime]

    region: Mapped["Region"] = relationship(
        back_populates="weather", foreign_keys=[region_id]
    )
    forecasts: Mapped[list["Forecast"]] = relationship(
        back_populates="weather",
        secondary=weather_forecast_table,
        cascade="save-update, merge, delete",
    )
