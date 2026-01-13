from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.api.v1.routers import (
    auth_router,
    movie_router,
    user_router,
)
from app.core import settings

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(
    router=auth_router,
    dependencies=[
        Depends(RateLimiter(seconds=5)),
    ],
)
router.include_router(
    router=movie_router,
    dependencies=[
        Depends(RateLimiter(seconds=1)),
    ],
)
router.include_router(
    router=user_router,
    dependencies=[
        Depends(RateLimiter(seconds=1)),
    ],
)
