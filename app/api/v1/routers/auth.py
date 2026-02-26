from fastapi import (
    APIRouter,
    status,
)

from app.api.v1.dependencies import (
    AuthLoginDep,
    AuthLogoutDep,
    AuthRegisterDep,
)
from app.api.v1.schemas import (
    BaseResponse,
    ResponseRegisterNewUser,
    ResponseSuccessLogin,
    ResponseSuccessLogout,
)
from app.core import (
    dep_rate_limiter_getter,
    settings,
)

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
    dependencies=[
        dep_rate_limiter_getter(seconds=5, limit=2),
    ],
)


@router.post(
    path="/login",
    response_model=ResponseSuccessLogin,
)
async def login(
    login_status: AuthLoginDep,
) -> BaseResponse:
    """
    Log in to the account.

    Parameters
    ----------
    login_status : AuthLoginDep
        login status message

    Returns
    -------
    BaseResponse
        status message
    """
    return login_status


@router.post(
    path="/register",
    response_model=ResponseRegisterNewUser,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    register_status: AuthRegisterDep,
) -> BaseResponse:
    """
    Register a new user.

    Parameters
    ----------
    register_status : AuthRegisterDep
        register status message

    Returns
    -------
    BaseResponse
        status message
    """
    return register_status


@router.get(
    path="/logout",
    response_model=ResponseSuccessLogout,
)
async def logout(
    logout_status: AuthLogoutDep,
) -> BaseResponse:
    """
    Log out of the account.

    Parameters
    ----------
    logout_status : AuthLogoutDep
        logout status message

    Returns
    -------
    BaseResponse
        status message
    """
    return logout_status
