from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(include_in_schema=False)


@router.get("/")
def redirect_root() -> RedirectResponse:
    """Redirect the root page '/' to the doc page '/docs'.

    Returns
    -------
    RedirectResponse
        redirect response (307)
    """
    return RedirectResponse("/docs")
