from datetime import datetime
from typing import Annotated

from annotated_types import Ge
from pydantic import BaseModel, ConfigDict, Field

from if_else_2024.forecasts.models import WeatherCondition


class ForecastDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_time: Annotated[datetime, Field(serialization_alias="dateTime")]
    temperature: float
    weather_condition: Annotated[
        WeatherCondition, Field(serialization_alias="weatherCondition")
    ]
    region_id: Annotated[int, Field(serialization_alias="regionId")]


class CreateForecastDto(BaseModel):
    region_id: Annotated[int, Ge(1), Field(validation_alias="regionId")]
    date_time: Annotated[datetime, Field(validation_alias="dateTime")]
    temperature: float
    weather_condition: Annotated[
        WeatherCondition, Field(validation_alias="weatherCondition")
    ]


class UpdateForecastDto(BaseModel):
    temperature: float
    weather_condition: Annotated[
        WeatherCondition, Field(validation_alias="weatherCondition")
    ]
    date_time: Annotated[datetime, Field(validation_alias="dateTime")]
