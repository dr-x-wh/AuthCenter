from typing import Literal

from pydantic import Field, IPvAnyAddress, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["error", "warning", "info", "debug"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
        frozen=True,
        hide_input_in_errors=True,
    )

    environment: Literal["development", "production"] = Field(validation_alias="BACKEND_ENV")
    host: IPvAnyAddress = Field(validation_alias="UVICORN_HOST")
    port: int = Field(ge=1, le=65535, validation_alias="UVICORN_PORT")

    database_url: str = Field(validation_alias="DATABASE_URL", min_length=1, repr=False)
    redis_url: str = Field(validation_alias="REDIS_URL", min_length=1, repr=False)

    log_level: LogLevel = Field(default="info", validation_alias="UVICORN_LOG_LEVEL")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, level: LogLevel, info: ValidationInfo) -> LogLevel:
        if level == "debug" and info.data.get("environment") == "production":
            raise ValueError("debug is only allowed when BACKEND_ENV=development")
        return level
