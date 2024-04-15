from datetime import datetime
from typing import Annotated, Any

from annotated_types import Ge
from pydantic import AliasPath, BaseModel, BeforeValidator, ConfigDict, Field

from if_else_2024.forecasts.models import Forecast
from if_else_2024.utils import NonEmptyStr
from if_else_2024.weather.models import WeatherCondition


def convert_weather_forecast_to_ids(v: Any) -> list[int]:
    assert isinstance(v, list)
    a = []
    for forecast in v:
        assert isinstance(forecast, Forecast)
        a.append(forecast.id)
    return a


class WeatherDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    region_name: Annotated[
        str,
        Field(
            serialization_alias="regionName",
            validation_alias=AliasPath("region", "name"),
        ),
    ]
    temperature: float
    humidity: float
    wind_speed: Annotated[float, Field(serialization_alias="windSpeed")]
    weather_condition: Annotated[
        WeatherCondition, Field(serialization_alias="weatherCondition")
    ]
    precipitation_amount: Annotated[
        float, Field(serialization_alias="precipitationAmount")
    ]
    measurement_date_time: Annotated[
        datetime, Field(serialization_alias="measurementDateTime")
    ]
    weather_forecast: Annotated[
        list[int],
        Field(serialization_alias="weatherForecast", validation_alias="forecasts"),
        BeforeValidator(convert_weather_forecast_to_ids),
    ]


class CreateWeatherDto(BaseModel):
    region_id: Annotated[int, Field(validation_alias="regionId"), Ge(1)]
    temperature: float
    humidity: float
    wind_speed: Annotated[float, Field(validation_alias="windSpeed"), Ge(0)]
    weather_condition: Annotated[
        WeatherCondition, Field(validation_alias="weatherCondition")
    ]
    precipitation_amount: Annotated[
        float, Field(validation_alias="precipitationAmount"), Ge(0)
    ]
    measurement_date_time: Annotated[
        datetime, Field(validation_alias="measurementDateTime")
    ]
    weather_forecast: Annotated[list[int], Field(validation_alias="weatherForecast")]


class UpdateWeatherDto(BaseModel):
    region_name: Annotated[str, NonEmptyStr]
    temperature: float
    humidity: float
    wind_speed: Annotated[float, Field(validation_alias="windSpeed"), Ge(0)]
    weather_condition: Annotated[
        WeatherCondition, Field(validation_alias="weatherCondition")
    ]
    precipitation_amount: Annotated[
        float, Field(validation_alias="precipitationAmount"), Ge(0)
    ]
    measurement_date_time: Annotated[
        datetime, Field(validation_alias="measurementDateTime")
    ]
    weather_forecast: Annotated[list[int], Field(validation_alias="weatherForecast")]
