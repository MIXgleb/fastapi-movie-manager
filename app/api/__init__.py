from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.api.v1 import router as api_v1_router
from app.core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
    dependencies=[Depends(RateLimiter(seconds=5))],
)
router.include_router(api_v1_router)
