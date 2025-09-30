from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Response,
    status,
)
from fastapi_limiter.depends import RateLimiter

from app.api.v1.schemas import (
    LoginResponse,
    LogoutResponse,
    RegisterResponse,
    UserInputDTO,
)
from app.core.config import settings
from app.core.security import TokensFromCookie
from app.services import (
    AuthService,
    AuthServiceBase,
    SqlAlchemyServiceHelper,
)

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
    dependencies=[Depends(RateLimiter(seconds=10))],
)
auth_service_helper = SqlAlchemyServiceHelper(AuthService)

AuthServiceType = Annotated[
    AuthServiceBase,
    Depends(auth_service_helper.service_getter),
]
UserFromBody = Annotated[UserInputDTO, Body()]


@router.post("/login")
async def login(
    auth_service: AuthServiceType,
    user_input: UserFromBody,
    response: Response,
) -> LoginResponse:
    """Log in to the account.

    Parameters
    ----------
    auth_service : AuthServiceBase
        auth service

    user_input : UserInputDTO
        user credentials

    response : Response
        response from the endpoint

    Returns
    -------
    LoginResponse
        status message
    """
    await auth_service.login(user_input, response)
    return LoginResponse()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    auth_service: AuthServiceType,
    user_input: UserFromBody,
) -> RegisterResponse:
    """Register a new user.

    Parameters
    ----------
    auth_service : AuthServiceBase
        auth service

    user_input : UserInputDTO
        user credentials

    Returns
    -------
    RegisterResponse
        status message
    """
    await auth_service.register(user_input)
    return RegisterResponse()


@router.get("/logout")
async def logout(
    auth_service: AuthServiceType,
    tokens: TokensFromCookie,
    response: Response,
) -> LogoutResponse:
    """Log out of the account.

    Parameters
    ----------
    auth_service : AuthServiceType
        auth service

    tokens : TokenReadDTO
        client's tokens

    response : Response
        response from the endpoint

    Returns
    -------
    LogoutResponse
        status message
    """
    await auth_service.logout(tokens, response)
    return LogoutResponse()
