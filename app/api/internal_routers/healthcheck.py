from fastapi import (
    APIRouter,
    Response,
)
from fastapi.responses import (
    JSONResponse,
)

from app.core import (
    dep_rate_limiter_getter,
)

router = APIRouter(
    tags=["Health"],
    dependencies=[
        dep_rate_limiter_getter(seconds=1),
    ],
)


@router.get(
    path="/healthcheck",
)
async def health_check() -> Response:
    """
    Check the health of the application.

    Returns
    -------
    Response
        status message
    """
    return JSONResponse(
        content={
            "message": "Success.",
        }
    )
