from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "QuickTrust"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    # Database — defaults to SQLite for local dev, use postgresql+asyncpg://... for production
    DATABASE_URL: str = "sqlite+aiosqlite:///./quicktrust.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Keycloak
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "quicktrust"
    KEYCLOAK_CLIENT_ID: str = "quicktrust-api"
    KEYCLOAK_CLIENT_SECRET: str = "quicktrust-api-secret"

    # MinIO
    MINIO_URL: str = "http://localhost:9000"
    MINIO_ROOT_USER: str = "quicktrust"
    MINIO_ROOT_PASSWORD: str = "quicktrust_dev"
    MINIO_BUCKET: str = "quicktrust-evidence"

    # LiteLLM
    LITELLM_MODEL: str = "gpt-4o-mini"
    OPENAI_API_KEY: str = ""

    # Prowler
    PROWLER_OUTPUT_DIR: str = "/tmp/prowler-output"
    PROWLER_TIMEOUT_SECONDS: int = 3600

    # SMTP email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "notifications@quicktrust.dev"
    SMTP_USE_TLS: bool = True

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
