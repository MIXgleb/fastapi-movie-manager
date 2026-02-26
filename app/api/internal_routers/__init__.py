__all__ = ("router",)

from fastapi import (
    APIRouter,
)

from app.api.internal_routers.healthcheck import (
    router as health_router,
)

router = APIRouter(tags=["Internal"])
router.include_router(health_router)
