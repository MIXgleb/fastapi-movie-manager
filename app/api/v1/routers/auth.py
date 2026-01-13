from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Request,
    Response,
    status,
)
from pydantic import BaseModel

from app.api.v1.schemas import (
    LoginResponse,
    LogoutResponse,
    RegisterResponse,
    UserInputDTO,
)
from app.core import settings
from app.services import (
    AuthService,
    BaseAuthService,
    SqlAlchemyServiceHelper,
)

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)
auth_service_helper = SqlAlchemyServiceHelper(AuthService)

AuthServiceType = Annotated[
    BaseAuthService,
    Depends(auth_service_helper.service_getter),
]
UserFromBody = Annotated[UserInputDTO, Body()]


@router.post(path="/login")
async def login(
    auth_service: AuthServiceType,
    user_input: UserFromBody,
    request: Request,
) -> BaseModel:
    """Log in to the account.

    Parameters
    ----------
    auth_service : BaseAuthService
        auth service

    user_input : UserInputDTO
        user credentials

    request : Request
        request from the client

    Returns
    -------
    BaseModel
        status message
    """
    await auth_service.login(user_input, request)
    return LoginResponse()


@router.post(path="/register", status_code=status.HTTP_201_CREATED)
async def register(
    auth_service: AuthServiceType,
    user_input: UserFromBody,
) -> BaseModel:
    """Register a new user.

    Parameters
    ----------
    auth_service : BaseAuthService
        auth service

    user_input : UserInputDTO
        user credentials

    Returns
    -------
    BaseModel
        status message
    """
    await auth_service.register(user_input)
    return RegisterResponse()


@router.get(path="/logout")
async def logout(
    auth_service: AuthServiceType,
    request: Request,
    response: Response,
) -> BaseModel:
    """Log out of the account.

    Parameters
    ----------
    auth_service : AuthServiceType
        auth service

    request : Request
        request from the client

    response : Response
        response to the client

    Returns
    -------
    BaseModel
        status message
    """
    await auth_service.logout(request, response)
    return LogoutResponse()
