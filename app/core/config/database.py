from functools import (
    cached_property,
)

from pydantic import (
    BaseModel as BaseSchema,
)
from pydantic.types import (
    SecretStr,
)
from sqlalchemy.engine import (
    URL,
)


class SqlAlchemyConfig(BaseSchema):
    """SQLAlchemy connection configuration."""

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class DatabaseConfig(BaseSchema):
    """Database configuration."""

    username: str = "app"
    host: str = "localhost"
    port: int = 5432
    database: str = "movie_manager"
    password: SecretStr

    sqla: SqlAlchemyConfig = SqlAlchemyConfig()

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @cached_property
    def async_url(self) -> URL:
        """Database url connection."""
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.database,
        )
