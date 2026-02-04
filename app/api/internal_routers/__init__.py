__all__ = ("router",)

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.api.internal_routers.health import router as health_router

router = APIRouter(
    dependencies=[
        Depends(RateLimiter(seconds=1)),
    ],
)
router.include_router(health_router)
