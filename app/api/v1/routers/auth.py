from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, status

from app.api.v1.schemas import MessageLoginReturn, MessageRegisterReturn
from app.core.config import settings
from app.schemas import UserInput
from app.services import AuthService, AuthServiceBase, SqlAlchemyServiceHelper

router = APIRouter(prefix=settings.api.v1.auth, tags=["Auth"])
auth_service_helper = SqlAlchemyServiceHelper(AuthService)


@router.post("/login", response_model=MessageLoginReturn)
async def login(
    auth_service: Annotated[AuthServiceBase, Depends(auth_service_helper.service_getter)],
    user_input: Annotated[UserInput, Body()],
    response: Response,
):
    """Log in to the account.

    Parameters
    ----------
    auth_service : AuthServiceBase
        auth service

    user_input : UserInput
        user credentials

    response : Response
        response to the client

    Returns
    -------
    MessageLoginReturn
        status message
    """
    await auth_service.login(user_input, response)
    return MessageLoginReturn()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=MessageRegisterReturn)
async def register(
    auth_service: Annotated[AuthServiceBase, Depends(auth_service_helper.service_getter)],
    user_input: Annotated[UserInput, Body()],
):
    """Register a new user.

    Parameters
    ----------
    auth_service : AuthServiceBase
        auth service

    user_input : UserInput
        user credentials

    Returns
    -------
    MessageRegisterReturn
        status message
    """
    await auth_service.register(user_input)
    return MessageRegisterReturn()
