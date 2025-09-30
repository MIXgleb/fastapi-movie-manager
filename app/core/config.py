from datetime import timedelta
from pathlib import Path
from typing import Final, Self

from loguru import logger
from pydantic import (
    BaseModel,
    Field,
    PostgresDsn,
    computed_field,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class _LoggerConfig(BaseModel):
    enabled: bool = True
    level: str = "INFO"
    path: str = "logs/{time:YYYY-MM-DD}/log.log"
    rotation: str = "00:00"
    retention: str = "30 days"

    @field_validator("level")
    @classmethod
    def validate_level(cls, level: str) -> str:
        valid_levels = {
            "TRACE",
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }

        if level.upper() not in valid_levels:
            exc_msg = f"Invalid log level. Must be one of: {valid_levels}"
            raise ValueError(exc_msg)

        return level.upper()


class _LoggingConfig(BaseModel):
    stream: _LoggerConfig
    common_file: _LoggerConfig
    error_file: _LoggerConfig
    json_file: _LoggerConfig

    stream_log_handler: int | None = None
    common_log_handler: int | None = None
    error_log_handler: int | None = None
    json_log_handler: int | None = None

    path_folder: Path = Field(
        default=Path("logs").resolve(),
        description="The path to the logs folder.",
    )

    @model_validator(mode="after")
    def create_log_folder(self) -> Self:
        self.path_folder.mkdir(exist_ok=True, parents=True)
        return self

    @model_validator(mode="after")
    def remove_existing_logger(self) -> Self:
        logger.remove()
        return self


class _TokenConfig(BaseModel):
    secret_jwt_key: str
    secret_fernet_key: str
    algorithm: str
    access_token_ttl: timedelta = timedelta(minutes=1)
    refresh_token_ttl: timedelta = timedelta(minutes=5)

    @computed_field
    @property
    def access_token_ttl_seconds(self) -> int:
        return int(self.access_token_ttl.total_seconds())

    @computed_field
    @property
    def refresh_token_ttl_seconds(self) -> int:
        return int(self.refresh_token_ttl.total_seconds())


class _RedisConfig(BaseModel):
    host: str
    port: int
    db_request_limiter: int
    db_refresh_token: int
    encoding: str = "utf8"

    @computed_field
    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"


class _RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class _ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    movies: str = "/movies"


class _ApiPrefix(BaseModel):
    prefix: str = "/api"
    health: str = "/health"
    v1: _ApiV1Prefix = _ApiV1Prefix()


class _DatabaseConfig(BaseModel):
    username: str
    password: str
    host: str
    port: int
    tablename: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn(
            "postgresql+asyncpg://"
            f"{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.tablename}"
        )


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    token: _TokenConfig
    db: _DatabaseConfig
    redis: _RedisConfig
    logging: _LoggingConfig
    debug: bool

    run: _RunConfig = _RunConfig()
    api: _ApiPrefix = _ApiPrefix()


settings: Final = _Settings()  # type: ignore[reportCallIssue]
DEBUG: Final[bool] = settings.debug
