from typing import Literal

from pydantic import IPvAnyAddress, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["ERROR", "WARNING", "INFO", "DEBUG"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    env: Literal["development", "production"]
    host: IPvAnyAddress
    port: int

    database_url: str
    redis_url: str

    log_level: LogLevel

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, level: LogLevel, info: ValidationInfo) -> LogLevel:
        if level == "debug" and info.data.get("environment") == "production":
            raise ValueError("debug is only allowed when BACKEND_ENV=development")
        return level.upper()
