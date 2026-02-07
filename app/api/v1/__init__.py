__all__ = ("router",)

from fastapi import APIRouter

from app.api.v1.routers import (
    auth_router,
    movie_router,
    user_router,
)
from app.core import dep_rate_limiter_getter, settings

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(
    router=auth_router,
    dependencies=[
        dep_rate_limiter_getter(seconds=5),
    ],
)
router.include_router(
    router=movie_router,
    dependencies=[
        dep_rate_limiter_getter(seconds=1),
    ],
)
router.include_router(
    router=user_router,
    dependencies=[
        dep_rate_limiter_getter(seconds=1),
    ],
)
