from typing import Literal

from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["ERROR", "WARNING", "INFO", "DEBUG"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", frozen=True)

    env: Literal["development", "production"]
    database_url: str
    redis_url: str

    log_level: LogLevel

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, level: LogLevel, info: ValidationInfo) -> LogLevel:
        if level == "DEBUG" and info.data.get("env") == "production":
            msg = "仅开发环境允许使用 DEBUG 日志级别"
            raise ValueError(msg)
        return level


settings = Settings()
