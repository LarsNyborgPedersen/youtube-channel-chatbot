from functools import lru_cache
from typing import List, Union

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = Field(default="development")

    # CORS - use Union to handle both string and list
    cors_allow_origins: Union[List[str], str] = Field(
        default="http://localhost:3000,http://127.0.0.1:3000"
    )

    # Timeouts
    request_timeout_seconds: int = 60

    # YouTube Data API (optional for demo mode)
    youtube_api_key: str = Field(default="", description="YouTube Data API v3 key (optional for demo mode)")

    @field_validator('cors_allow_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    class Config:
        env_file = ".env"
        env_prefix = "APP_"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


