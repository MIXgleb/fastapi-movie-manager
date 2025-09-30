from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from fastapi_limiter.depends import RateLimiter

from app.core.config import settings

router = APIRouter(
    prefix=settings.api.health,
    tags=["Health"],
    dependencies=[Depends(RateLimiter(seconds=30))],
)


@router.get("/check")
def health_check() -> ORJSONResponse:
    """Check the health of the service.

    Returns
    -------
    json
        status message
    """
    return ORJSONResponse({"message": "Success."})
