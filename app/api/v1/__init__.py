from fastapi import APIRouter

from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.movies import router as movie_router
from app.api.v1.routers.users import router as user_router
from app.core.config import settings

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(auth_router)
router.include_router(movie_router)
router.include_router(user_router)
