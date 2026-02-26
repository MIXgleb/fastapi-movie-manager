__all__ = ("router",)

from fastapi import (
    APIRouter,
)

from app.api.v1.routers import (
    auth_router,
    movie_router,
    user_router,
)
from app.core import (
    settings,
)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    tags=["V1"],
)
router.include_router(auth_router)
router.include_router(movie_router)
router.include_router(user_router)
