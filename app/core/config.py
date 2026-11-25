from typing import Annotated, Literal

from pydantic import AnyUrl, Field, IPvAnyAddress, StringConstraints, UrlConstraints, field_validator
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
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

    environment: Literal["development", "production"] = Field(validation_alias="BACKEND_ENV")
    host: IPvAnyAddress = Field(validation_alias="BACKEND_HOST")
    port: int = Field(ge=1, le=65535, validation_alias="BACKEND_PORT")

    database_url: DatabaseURL = Field(validation_alias="DATABASE_URL")
    redis_url: RedisURL = Field(validation_alias="REDIS_URL")

    app_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = "AuthCenter"
    log_level: Literal["ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"

    @field_validator("log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, value: object) -> object:
        return value.strip().upper() if isinstance(value, str) else value
