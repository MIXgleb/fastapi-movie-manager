__all__ = (
    "api_v1_router",
    "common_router",
)

from app.api.common_routers import router as common_router
from app.api.v1 import router as api_v1_router
