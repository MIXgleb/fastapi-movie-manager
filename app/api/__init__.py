__all__ = ("router",)

from fastapi import (
    APIRouter,
)

from app.api.internal_routers import (
    router as internal_router,
)
from app.api.v1 import (
    router as api_v1_router,
)
from app.core import (
    settings,
)

router = APIRouter()
router.include_router(
    router=internal_router,
    prefix=settings.api.internal.prefix,
)
router.include_router(
    router=api_v1_router,
    prefix=settings.api.prefix,
)
