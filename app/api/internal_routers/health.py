from fastapi import APIRouter, Response
from fastapi.responses import ORJSONResponse

router = APIRouter(tags=["Health"])


@router.get(path="/healthcheck")
async def health_check() -> Response:
    """Check the health of the service.

    Returns
    -------
    Response
        status message
    """
    return ORJSONResponse({"message": "Success."})
