from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, ORJSONResponse

from app.core import DEBUG


async def _check_mode() -> None:  # noqa: RUF029
    """Check the access of documentation depending on the mode.

    Raises
    ------
    HTTPException
        page not found
    """
    if not DEBUG:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


router = APIRouter(
    include_in_schema=False,
    dependencies=[
        Depends(_check_mode),
    ],
)


@router.get(path="/docs")
async def call_docs() -> HTMLResponse:
    """Generate and return the HTML that loads Swagger UI for the interactive API docs.

    Returns
    -------
    HTMLResponse
        docs HTML
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
    )


@router.get(path="/docs/oauth2-redirect")
async def call_docs_oauth2_redirect() -> HTMLResponse:
    """Generate the HTML response with the OAuth2 redirection for Swagger UI.

    Returns
    -------
    HTMLResponse
        docs HTML
    """
    return get_swagger_ui_oauth2_redirect_html()


@router.get(path="/redoc")
async def call_redoc() -> HTMLResponse:
    """Generate and return the HTML response that loads ReDoc for the alternative API docs.

    Returns
    -------
    HTMLResponse
        redoc HTML
    """
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="API Docs",
    )


@router.get(path="/openapi.json")
async def call_openapi(
    request: Request,
) -> Response:
    """Generate and return the OpenAPI json.

    Parameters
    ----------
    request : Request
        request from the client

    Returns
    -------
    Response
        OpenAPI json
    """
    return ORJSONResponse(
        get_openapi(
            title=f"{request.app.title} API Docs",
            version=request.app.version,
            routes=request.app.routes,
            summary=request.app.summary,
            description=request.app.description,
        )
    )
