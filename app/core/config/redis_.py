from pydantic import (
    BaseModel as BaseSchema,
)


class RedisConfig(BaseSchema):
    """Redis configuration."""

    host: str = "localhost"
    port: int = 6379
    db_refresh_token: int = 1
    encoding: str = "utf-8"
