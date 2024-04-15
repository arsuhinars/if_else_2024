from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_url: str
    server_url: str | None = None
    cors_allowed_origins: list[str]
    auth_session_lifetime: int = 3600

    create_fake_data: bool = False
    fake_accounts_count: int = 100
    fake_region_types_count: int = 10
    fake_regions_count: int = 100
    fake_forecasts_count: int = 100
    fake_weather_count: int = 100
