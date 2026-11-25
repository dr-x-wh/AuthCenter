from functools import cache
from typing import Literal

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

    app_name: str = "AuthCenter"
    app_debug: bool = False

    log_level: Literal["ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"

    postgres_url: str = Field(validation_alias=AliasChoices("postgres_url", "database_url"))
    redis_url: str

    @field_validator("log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, value: object) -> object:
        return value.strip().upper() if isinstance(value, str) else value


@cache
def get_settings() -> Settings:
    return Settings()
