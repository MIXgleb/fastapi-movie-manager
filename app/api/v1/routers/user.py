from collections.abc import Sequence
from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Path,
    Query,
    Request,
    Response,
    status,
)
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.api.v1.dependencies import (
    UserOwnership,
    dep_permission_getter,
)
from app.api.v1.schemas import (
    DeleteUserResponse,
    UpdateUserResponse,
    UserFilterDTO,
    UserOutputDTO,
    UserUpdateDTO,
)
from app.core.config import settings
from app.core.security import PayloadFromToken
from app.domains import UserRole
from app.services import (
    BaseUserService,
    SqlAlchemyServiceHelper,
    UserService,
)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)
user_service_helper = SqlAlchemyServiceHelper(UserService)

UserServiceType = Annotated[
    BaseUserService,
    Depends(user_service_helper.service_getter),
]
UserIdFromPath = Annotated[int, Path()]
UserFilterFromQuery = Annotated[UserFilterDTO, Query()]
UserUpdateFromBody = Annotated[UserUpdateDTO, Body()]


@router.get("/me")
async def get_me(
    payload: PayloadFromToken,
    request: Request,
) -> RedirectResponse:
    """Get my user's information.

    Parameters
    ----------
    payload : Payload
        payload data

    request : Request
        request to the endpoint

    Returns
    -------
    RedirectResponse
        redirect response (308)
    """
    return RedirectResponse(
        url=request.url.path.removesuffix("/me") + f"/{payload.user_id}",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )


@router.put("/me")
async def update_me(
    payload: PayloadFromToken,
    request: Request,
) -> RedirectResponse:
    """Update my user's information.

    Parameters
    ----------
    payload : Payload
        payload data

    request : Request
        request to the endpoint

    Returns
    -------
    RedirectResponse
        redirect response (308)
    """
    return RedirectResponse(
        url=request.url.path.removesuffix("/me") + f"/{payload.user_id}",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )


@router.delete("/me")
async def delete_me(
    payload: PayloadFromToken,
    request: Request,
) -> RedirectResponse:
    """Delete my account.

    Parameters
    ----------
    payload : Payload
        payload data

    request : Request
        request to the endpoint

    Returns
    -------
    RedirectResponse
        redirect response (308)
    """
    return RedirectResponse(
        url=request.url.path.removesuffix("/me") + f"/{payload.user_id}",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )


@router.get(
    "/all",
    dependencies=[dep_permission_getter(UserRole.admin)],
)
async def get_all_users(
    user_service: UserServiceType,
    filters: UserFilterFromQuery,
) -> Sequence[UserOutputDTO]:
    """Get all users.

    Parameters
    ----------
    user_service : BaseUserService
        user service

    filters : UserFilterDTO
        user search filter

    Returns
    -------
    Sequence[UserOutputDTO]
        data of users
    """
    return await user_service.get_all_users(filters)


@router.get(
    "/{user_id}",
    dependencies=[UserOwnership],
)
async def get_user(
    user_service: UserServiceType,
    user_id: UserIdFromPath,
) -> UserOutputDTO:
    """Get user's information by id.

    Parameters
    ----------
    user_service : BaseUserService
        user service

    user_id : int
        user id

    Returns
    -------
    UserOutputDTO
        user data
    """
    return await user_service.get_user(user_id)


@router.put(
    "/{user_id}",
    dependencies=[
        dep_permission_getter(UserRole.admin, UserRole.user),
        UserOwnership,
    ],
)
async def update_user(
    user_service: UserServiceType,
    user_id: UserIdFromPath,
    user_update: UserUpdateFromBody,
    request: Request,
    response: Response,
) -> BaseModel:
    """Update the user by id.

    Parameters
    ----------
    user_service : UserServiceType
        user service

    user_id : int
        user id

    user_update : UserUpdateDTO
        user data to update

    request : Request
        request to the endpoint

    response : Response
        response from the endpoint

    Returns
    -------
    BaseModel
        status message
    """
    await user_service.update_user(
        user_id=user_id,
        user_update=user_update,
        request=request,
        response=response,
    )
    return UpdateUserResponse()


@router.delete(
    "/{user_id}",
    dependencies=[
        dep_permission_getter(UserRole.admin, UserRole.user),
        UserOwnership,
    ],
)
async def delete_user(
    user_service: UserServiceType,
    user_id: UserIdFromPath,
    request: Request,
    response: Response,
) -> BaseModel:
    """Delete user by id.

    Parameters
    ----------
    user_service : BaseUserService
        user service

    user_id : int
        user id

    request : Request
        request to the endpoint

    response : Response
        response from the endpoint

    Returns
    -------
    BaseModel
        status message
    """
    user = await user_service.delete_user(
        user_id=user_id,
        request=request,
        response=response,
    )
    return DeleteUserResponse(user=user)
