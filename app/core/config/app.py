from pydantic import (
    BaseModel as BaseSchema,
)


class AppConfig(BaseSchema):
    """Application configuration."""

    title: str = "Movie Manager"
    host: str = "127.0.0.1"
    port: int = 8000
