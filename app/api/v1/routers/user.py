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
)
from fastapi.responses import RedirectResponse
from fastapi_limiter.depends import RateLimiter

from app.api.v1.dependencies import (
    PayloadByToken,
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
from app.core.security import TokensFromCookie
from app.domains import UserRole
from app.services import (
    SqlAlchemyServiceHelper,
    UserService,
    UserServiceBase,
)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
    dependencies=[Depends(RateLimiter(seconds=5))],
)
user_service_helper = SqlAlchemyServiceHelper(UserService)

UserServiceType = Annotated[
    UserServiceBase,
    Depends(user_service_helper.service_getter),
]
UserIdFromPath = Annotated[int, Path()]
UserFilterFromQuery = Annotated[UserFilterDTO, Query()]
UserUpdateFromBody = Annotated[UserUpdateDTO, Body()]


@router.get("/me")
async def get_me(
    payload: PayloadByToken,
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
        redirect response (307)
    """
    return RedirectResponse(request.url.path.removesuffix("/me") + f"/{payload.user_id}")


@router.put(
    "/me",
    dependencies=[
        dep_permission_getter(UserRole.admin, UserRole.user),
        UserOwnership,
    ],
)
async def update_me(
    payload: PayloadByToken,
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
        redirect response (307)
    """
    return RedirectResponse(request.url.path.removesuffix("/me") + f"/{payload.user_id}")


@router.delete(
    "/me",
    dependencies=[
        dep_permission_getter(UserRole.admin, UserRole.user),
        UserOwnership,
    ],
)
async def delete_me(
    payload: PayloadByToken,
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
        redirect response (307)
    """
    return RedirectResponse(request.url.path.removesuffix("/me") + f"/{payload.user_id}")


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
    user_service : UserServiceBase
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
    user_service : UserServiceBase
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
    tokens: TokensFromCookie,
    response: Response,
) -> UpdateUserResponse:
    """Update the user by id.

    Parameters
    ----------
    user_service : UserServiceType
        user service

    user_id : int
        user id

    user_update : UserUpdateDTO
        user data to update

    tokens : TokenReadDTO
        client's tokens

    response : Response
        response from the endpoint

    Returns
    -------
    UpdateUserResponse
        status message
    """
    await user_service.update_user(user_id, user_update, tokens, response)
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
    tokens: TokensFromCookie,
    response: Response,
) -> DeleteUserResponse:
    """Delete user by id.

    Parameters
    ----------
    user_service : UserServiceBase
        user service

    user_id : int
        user id

    tokens : TokenReadDTO
        client's tokens

    response : Response
        response from the endpoint

    Returns
    -------
    DeleteUserResponse
        status message
    """
    user = await user_service.delete_user(user_id, tokens, response)
    return DeleteUserResponse(user=user)
