__all__ = (
    "auth_router",
    "movie_router",
    "user_router",
)

from app.api.v1.routers.auth import (
    router as auth_router,
)
from app.api.v1.routers.movie import (
    router as movie_router,
)
from app.api.v1.routers.user import (
    router as user_router,
)
