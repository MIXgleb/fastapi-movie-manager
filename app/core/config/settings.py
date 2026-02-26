from pathlib import (
    Path,
)
from typing import (
    Final,
    override,
)

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from app.core.config.api import (
    ApiConfig,
)
from app.core.config.app import (
    AppConfig,
)
from app.core.config.database import (
    DatabaseConfig,
)
from app.core.config.logging_ import (
    LoggingConfig,
)
from app.core.config.redis_ import (
    RedisConfig,
)
from app.core.config.security import (
    AuthTokenConfig,
)

CONFIG_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent.parent
ENVS_DIR: Final[Path] = CONFIG_DIR / "envs"
YAML_DIR: Final[Path] = CONFIG_DIR / "yaml"


class Settings(BaseSettings):
    """Main config settings."""

    debug: bool
    db: DatabaseConfig
    auth_token: AuthTokenConfig
    logging: LoggingConfig

    app: AppConfig = AppConfig()
    redis: RedisConfig = RedisConfig()
    api: ApiConfig = ApiConfig()

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="MOVIE_MANAGER__",
        env_nested_delimiter="__",
        env_file=(
            ENVS_DIR / ".env.template",
            ENVS_DIR / ".env",
        ),
    )

    @classmethod
    @override
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


settings: Final = Settings()  # type: ignore[reportCallIssue]
DEBUG: Final[bool] = settings.debug
