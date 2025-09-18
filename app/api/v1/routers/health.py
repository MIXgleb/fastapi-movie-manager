from fastapi import APIRouter

from app.api.v1.schemas import MessageHealthCheckReturn
from app.core.config import settings

router = APIRouter(prefix=settings.api.v1.health, tags=["Health"])


@router.get("/check", response_model=MessageHealthCheckReturn)
def health_check():
    """Check the health of the service.

    Returns
    -------
    MessageHealthCheckReturn
        status message
    """
    return MessageHealthCheckReturn()
