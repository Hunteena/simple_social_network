from functools import lru_cache
from typing import Optional, List

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import PositiveInt, SecretStr

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    """Server settings.

    Formed from `.env` or `.env.dev`.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # #: SecretStr: secret x-token for authority.
    # X_API_TOKEN: SecretStr
    # #: str: Trusted host.
    # API_TRUSTED_HOST: str

    #: str: Postgresql host.
    POSTGRES_HOST: str
    #: PositiveInt: positive int (x > 0) port of postgresql.
    POSTGRES_PORT: PositiveInt
    #: str: Postgresql user.
    POSTGRES_USER: str
    # TODO SecretStr
    #: SecretStr: Postgresql password.
    POSTGRES_PASSWORD: str
    #: str: Postgresql database name.
    POSTGRES_DB: str

    #: Secret key for decode JWT
    SECRET_KEY: SecretStr

    # #: CORS
    # CORS_ALLOW_ORIGIN: Optional[List]
    # CORS_ALLOW_METHODS: Optional[List]
    # CORS_ALLOW_HEADERS: Optional[List]
    # CORS_ALLOW_CREDENTIALS: Optional[bool]

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def dsn(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))
