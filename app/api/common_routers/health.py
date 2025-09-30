from fastapi import APIRouter, Response
from fastapi.responses import ORJSONResponse

from app.core.config import settings

router = APIRouter(
    prefix=settings.api.health,
    tags=["Health"],
)


@router.get("/check")
def health_check() -> Response:
    """Check the health of the service.

    Returns
    -------
    Response
        status message
    """
    return ORJSONResponse({"message": "Success."})
