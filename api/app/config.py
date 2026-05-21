from pydantic import field_validator
from pydantic_core import PydanticCustomError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    port: int
    database_url: str
    redis_url: str = "redis://localhost:6379/0"

    @field_validator("port")
    @classmethod
    def validate_port(cls, value: int | str) -> int:
        try:
            port = int(value)
        except (TypeError, ValueError) as exc:
            raise PydanticCustomError(
                +
                "invalid_port",
                "Invalid PORT. Set PORT in .env to a positive integer, for example PORT=8000.",
            ) from exc

        value = port
        if value <= 0:
            raise PydanticCustomError(
                "invalid_port",
                "Invalid PORT. Set PORT in .env to a positive integer, for example PORT=8000.",
            )
        return value

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value or not value.strip():
            raise PydanticCustomError(
                "invalid_database_url",
                "Invalid DATABASE_URL. Set DATABASE_URL in .env to your local Postgres connection string.",
            )
        return value


settings = Settings()
