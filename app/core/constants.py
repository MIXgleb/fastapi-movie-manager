from collections.abc import (
    Sequence,
)
from typing import (
    Final,
)

from fastapi import (
    Response,
    status,
)
from fastapi.responses import (
    JSONResponse,
)
from pydantic.fields import (
    Field,
)

# ===========================================================================
# Logging
# ===========================================================================
EXTERNAL_LOGGERS: Final[Sequence[str]] = (
    # -------------------
    # FastAPI and Uvicorn
    # -------------------
    "uvicorn",
    "uvicorn.error",
    "fastapi",
    # -------------------
    # SQLAlchemy
    # -------------------
    "sqlalchemy",
    "sqlalchemy.engine",
    "sqlalchemy.pool",
    "sqlalchemy.orm",
    # -------------------
    # Alembic
    # -------------------
    "alembic",
    # -------------------
    # AsyncPG
    # -------------------
    "asyncpg",
    # -------------------
    # Redis
    # -------------------
    "redis",
    "redis.client",
    # -------------------
    # HTTP clients
    # -------------------
    "httpx",
    "httpcore",
    # -------------------
    # Security
    # -------------------
    "bcrypt",
    "cryptography",
)
DISABLED_LOGGERS: Final[Sequence[str]] = ("uvicorn.access",)


# ===========================================================================
# Schemas
# ===========================================================================
# ---------------------------------------------------------------------------
# Movie
# ---------------------------------------------------------------------------
MOVIE_TITLE_PATTERN: Final[str] = r"^[\w\s\d\.,!?@#%&*()_+\-=\[\]{}|;:\"<>`]+$"
MOVIE_DESCRIPTION_PATTERN: Final[str] = r"^[\w\s\d\.,!?@#%&*()_+\-=\[\]{}|;:\"<>`]+$"
MOVIE_TITLE_FIELD: Final = Field(max_length=30, pattern=MOVIE_TITLE_PATTERN)
MOVIE_DESCRIPTION_FIELD: Final = Field(
    default="",
    max_length=100,
    pattern=MOVIE_DESCRIPTION_PATTERN,
)
MOVIE_RATE_FIELD: Final = Field(ge=0, le=5)

# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------
USER_USERNAME_PATTERN: Final[str] = r"^[\w\d_\-]+$"
USER_USERNAME_FIELD: Final = Field(max_length=20, pattern=USER_USERNAME_PATTERN)
USER_PASSWORD_FIELD: Final = Field(min_length=5, max_length=30)


# ===========================================================================
# HTTP
# ===========================================================================
HTTP_RESPONSE_500: Final[Response] = JSONResponse(
    content={
        "error": "Internal server error.",
        "message": "Please try again later.",
    },
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
)
