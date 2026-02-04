__all__ = ("router",)

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.api.common_routers.docs import router as docs_router
from app.api.common_routers.health import router as health_router
from app.api.common_routers.root import router as root_router

router = APIRouter(
    dependencies=[
        Depends(RateLimiter(seconds=1)),
    ],
)
router.include_router(health_router)
router.include_router(docs_router)
router.include_router(root_router)
