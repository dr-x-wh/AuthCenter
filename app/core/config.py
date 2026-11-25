from typing import Annotated, Literal

from pydantic import AnyUrl, Field, IPvAnyAddress, StringConstraints, UrlConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict

DatabaseURL = Annotated[
    AnyUrl,
    UrlConstraints(
        allowed_schemes=["postgresql+asyncpg", "postgresql", "postgres"],
        host_required=True,
    ),
]
RedisURL = Annotated[
    AnyUrl,
    UrlConstraints(allowed_schemes=["redis", "rediss"], host_required=True),
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
        hide_input_in_errors=True,
    )

    environment: Literal["development", "production"] = Field(validation_alias="BACKEND_ENV")
    host: IPvAnyAddress = Field(validation_alias="UVICORN_HOST")
    port: int = Field(ge=1, le=65535, validation_alias="UVICORN_PORT")

    database_url: DatabaseURL = Field(validation_alias="DATABASE_URL")
    redis_url: RedisURL = Field(validation_alias="REDIS_URL")

    app_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(
        default="AuthCenter",
        validation_alias="APP_NAME",
    )
    log_level: Literal["error", "warning", "info", "debug"] = Field(
        default="info",
        validation_alias="UVICORN_LOG_LEVEL",
    )
