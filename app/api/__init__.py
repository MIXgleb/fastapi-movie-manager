__all__ = (
    "api_v1_router",
    "internal_router",
)

from app.api.internal_routers import router as internal_router
from app.api.v1 import router as api_v1_router
