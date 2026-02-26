from pydantic import (
    BaseModel as BaseSchema,
)


class _ApiV1Prefix(BaseSchema):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    movies: str = "/movies"


class _ApiInternalPrefix(BaseSchema):
    prefix: str = "/internal"


class ApiConfig(BaseSchema):
    """API prefixes configuration."""

    prefix: str = "/api"
    internal: _ApiInternalPrefix = _ApiInternalPrefix()
    v1: _ApiV1Prefix = _ApiV1Prefix()
