from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_url: str
    server_url: str | None = None
    cors_allowed_origins: list[str]
    auth_session_lifetime: int = 3600
