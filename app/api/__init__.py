from fastapi import APIRouter

from app.api.common_routers import router as common_router
from app.api.v1 import router as api_v1_router
from app.core.config import settings

router = APIRouter()
router.include_router(
    router=api_v1_router,
    prefix=settings.api.prefix,
)
router.include_router(common_router)
