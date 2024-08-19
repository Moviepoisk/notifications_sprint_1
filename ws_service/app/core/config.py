from pydantic_settings import BaseSettings, SettingsConfigDict


class WSServiceSettings(BaseSettings):
    """WS service settings for FastAPI project."""

    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="ws_service_",
        env_file_encoding="utf-8",
    )
    name: str = "ws_service"
    host: str = "ws_service"
    port: int = 8765
    workers: int = 1
    log_level: str = "info"


class RedisSettings(BaseSettings):
    """Redis settings class."""

    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="redis_",
        env_file_encoding="utf-8",
    )
    host: str = "redis"
    port: int = 6379


ws_service_settings = WSServiceSettings()
redis_settings = RedisSettings()
