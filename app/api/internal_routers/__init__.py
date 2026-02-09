__all__ = ("router",)

from fastapi import (
    APIRouter,
)

from app.api.internal_routers.health import (
    router as health_router,
)
from app.core import (
    dep_rate_limiter_getter,
)

router = APIRouter(
    dependencies=[
        dep_rate_limiter_getter(seconds=1),
    ],
)
router.include_router(health_router)
