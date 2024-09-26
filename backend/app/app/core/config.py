from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Any, Optional
from pydantic import AnyHttpUrl, field_validator, ValidationInfo
from starlette.middleware import Middleware
from starlette_context.middleware import ContextMiddleware
from starlette_context import plugins


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"

    PROJECT_NAME: str
    DOMAIN: str
    VERSION: str
    API_VERSION: str
    API_NAME: str
    API_VERSION_STR: Optional[str] = None

    @field_validator("API_VERSION_STR", mode="before")
    def assemble_version_str(cls, v: Optional[str], values: ValidationInfo) -> Any:
        return f"/{values.data.get('API_NAME')}/{values.data.get('API_VERSION')}"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    MIDDLEWARES: list = [
        Middleware(
            ContextMiddleware,
            plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
        )
    ]

    TEMP_DIR: str = "temp"


settings = get_settings()
