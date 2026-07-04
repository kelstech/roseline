from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="EHIS_", env_file=".env", extra="ignore")

    env: str = Field(default="local")
    service_name: str = Field(default="ehis-core")
    database_url: str = Field(default="sqlite+aiosqlite:///./ehis.db")
    allowed_origins: str = Field(default="http://localhost:5173")
    log_level: str = Field(default="INFO")
    auth_issuer: str = Field(default="https://identity.example.org")
    auth_audience: str = Field(default="ehis-api")
    storage_provider: str = Field(default="local")
    storage_local_path: str = Field(default="./data/documents")
    notification_outbox_enabled: bool = Field(default=True)

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
