from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "OpenComply"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: str = "http://localhost:3000"

    # Database — defaults to SQLite for local dev, use postgresql+asyncpg://... for production
    DATABASE_URL: str = "sqlite+aiosqlite:///./opencomply.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Keycloak
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "opencomply"
    KEYCLOAK_CLIENT_ID: str = "opencomply-api"
    KEYCLOAK_CLIENT_SECRET: str = "opencomply-api-secret"

    # MinIO
    MINIO_URL: str = "http://localhost:9000"
    MINIO_ROOT_USER: str = "opencomply"
    MINIO_ROOT_PASSWORD: str = "opencomply_dev"
    MINIO_BUCKET: str = "opencomply-evidence"

    # LiteLLM
    LITELLM_MODEL: str = "gpt-4o-mini"
    OPENAI_API_KEY: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
