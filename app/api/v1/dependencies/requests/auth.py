from typing import (
    Annotated,
)

from fastapi import (
    Body,
    Depends,
    Request,
    Response,
)

from app.api.v1.schemas import (
    BaseResponse,
    ResponseRegisterNewUser,
    ResponseSuccessLogin,
    ResponseSuccessLogout,
    UserInputDTO,
)
from app.core import (
    settings,
)
from app.domains import (
    UserInputDM,
)
from app.security.auth_managers import (
    AuthJWTManager,
)
from app.security.password_managers import (
    BcryptPasswordManager,
)
from app.services import (
    AuthService,
    BaseAuthService,
)
from app.services.service_managers import (
    SqlAlchemyServiceManager,
)

auth_service_manager = SqlAlchemyServiceManager(
    service_class=AuthService,
    password_manager=BcryptPasswordManager(),
    auth_manager=AuthJWTManager(
        auth_config=settings.auth_token,
    ),
)

AuthServiceDep = Annotated[
    BaseAuthService,
    Depends(auth_service_manager.service_getter),
]
UserFromBody = Annotated[UserInputDTO, Body()]


async def login(
    auth_service: AuthServiceDep,
    user_input: UserFromBody,
    request: Request,
) -> BaseResponse:
    """
    Log in to the account.

    Parameters
    ----------
    auth_service : AuthServiceDep
        auth service

    user_input : UserFromBody
        user credentials

    request : Request
        request from the client

    Returns
    -------
    BaseResponse
        status message
    """
    await auth_service.login(
        user_input=UserInputDM.from_object(user_input),
        request=request,
    )
    return ResponseSuccessLogin()


async def register(
    auth_service: AuthServiceDep,
    user_input: UserFromBody,
) -> BaseResponse:
    """
    Register a new user.

    Parameters
    ----------
    auth_service : AuthServiceDep
        auth service

    user_input : UserFromBody
        user credentials

    Returns
    -------
    BaseResponse
        status message
    """
    await auth_service.register(
        user_input=UserInputDM.from_object(user_input),
    )
    return ResponseRegisterNewUser()


async def logout(
    auth_service: AuthServiceDep,
    request: Request,
    response: Response,
) -> BaseResponse:
    """
    Log out of the account.

    Parameters
    ----------
    auth_service : AuthServiceDep
        auth service

    request : Request
        request from the client

    response : Response
        response to the client

    Returns
    -------
    BaseResponse
        status message
    """
    await auth_service.logout(
        request=request,
        response=response,
    )
    return ResponseSuccessLogout()


AuthLoginDep = Annotated[
    BaseResponse,
    Depends(login),
]
AuthRegisterDep = Annotated[
    BaseResponse,
    Depends(register),
]
AuthLogoutDep = Annotated[
    BaseResponse,
    Depends(logout),
]
