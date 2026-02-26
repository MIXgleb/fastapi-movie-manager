from collections.abc import (
    Sequence,
)
from typing import (
    Annotated,
)
from uuid import (
    UUID,
)

from fastapi import (
    Body,
    Depends,
    Path,
    Query,
    Request,
    Response,
    status,
)
from fastapi.responses import (
    RedirectResponse,
)

from app.api.v1.dependencies.security import (
    dep_user_ownership_getter,
)
from app.api.v1.schemas import (
    BaseResponse,
    ResponseDeleteUser,
    ResponseUpdateUser,
    UserFilterDTO,
    UserOutputDTO,
    UserUpdateDTO,
)
from app.core import (
    settings,
)
from app.domains import (
    UserFiltersDM,
    UserOutputDM,
    UserUpdateDM,
)
from app.security.auth_managers import (
    AuthJWTManager,
    PayloadDep,
)
from app.security.password_managers import (
    BcryptPasswordManager,
)
from app.services import (
    BaseUserService,
    UserService,
)
from app.services.service_managers import (
    SqlAlchemyServiceManager,
)

user_service_manager = SqlAlchemyServiceManager(
    service_class=UserService,
    password_manager=BcryptPasswordManager(),
    auth_manager=AuthJWTManager(
        auth_config=settings.auth_token,
    ),
)

UserServiceDep = Annotated[
    BaseUserService,
    Depends(user_service_manager.service_getter),
]
UserIdFromPath = Annotated[UUID, Path()]
UserFilterFromQuery = Annotated[UserFilterDTO, Query()]
UserUpdateFromBody = Annotated[UserUpdateDTO, Body()]


async def get_me(
    payload: PayloadDep,
    request: Request,
) -> RedirectResponse:
    """
    Get my user's information.

    Parameters
    ----------
    payload : PayloadDep
        payload data

    request : Request
        request from the client

    Returns
    -------
    RedirectResponse
        redirect response (308)
    """
    return RedirectResponse(
        url=request.url.path.removesuffix("/me") + f"/{payload.user_id}",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )


async def update_me(
    payload: PayloadDep,
    request: Request,
) -> RedirectResponse:
    """
    Update my user's information.

    Parameters
    ----------
    payload : PayloadDep
        payload data

    request : Request
        request from the client

    Returns
    -------
    RedirectResponse
        redirect response (308)
    """
    return RedirectResponse(
        url=request.url.path.removesuffix("/me") + f"/{payload.user_id}",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )


async def delete_me(
    payload: PayloadDep,
    request: Request,
) -> RedirectResponse:
    """
    Delete my account.

    Parameters
    ----------
    payload : PayloadDep
        payload data

    request : Request
        request from the client

    Returns
    -------
    RedirectResponse
        redirect response (308)
    """
    return RedirectResponse(
        url=request.url.path.removesuffix("/me") + f"/{payload.user_id}",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )


async def get_all_users(
    user_service: UserServiceDep,
    filters: UserFilterFromQuery,
) -> Sequence[UserOutputDM]:
    """
    Get all users.

    Parameters
    ----------
    user_service : UserServiceDep
        user service

    filters : UserFilterFromQuery
        user search filter

    Returns
    -------
    Sequence[UserOutputDM]
        data of users
    """
    return await user_service.get_all_users(
        filters=UserFiltersDM.from_object(filters),
    )


async def get_user(
    user_service: UserServiceDep,
    user_id: UserIdFromPath,
) -> UserOutputDM:
    """
    Get user's information by id.

    Parameters
    ----------
    user_service : UserServiceDep
        user service

    user_id : UserIdFromPath
        user id

    Returns
    -------
    UserOutputDM
        user data
    """
    return await user_service.get_user(
        user_id=user_id,
    )


async def update_user(
    user_service: UserServiceDep,
    user_id: UserIdFromPath,
    user_update: UserUpdateFromBody,
    request: Request,
    response: Response,
) -> BaseResponse:
    """
    Update a user by id.

    Parameters
    ----------
    user_service : UserServiceDep
        user service

    user_id : UserIdFromPath
        user id

    user_update : UserUpdateFromBody
        user data to update

    request : Request
        request from the client

    response : Response
        response to the client

    Returns
    -------
    BaseResponse
        status message
    """
    await user_service.update_user(
        user_id=user_id,
        user_update=UserUpdateDM.from_object(
            user_update.model_dump(exclude_unset=True),
            none_if_key_not_found=True,
        ),
        request=request,
        response=response,
    )
    return ResponseUpdateUser()


async def delete_user(
    user_service: UserServiceDep,
    user_id: UserIdFromPath,
    request: Request,
    response: Response,
) -> BaseResponse:
    """
    Delete user by id.

    Parameters
    ----------
    user_service : UserServiceDep
        user service

    user_id : UserIdFromPath
        user id

    request : Request
        request from the client

    response : Response
        response to the client

    Returns
    -------
    BaseResponse
        status message
    """
    user = await user_service.delete_user(
        user_id=user_id,
        request=request,
        response=response,
    )
    return ResponseDeleteUser(
        user=UserOutputDTO.model_validate(user),
    )


UserOwnershipDep = dep_user_ownership_getter()
UserGetMeDep = Annotated[
    RedirectResponse,
    Depends(get_me),
]
UserUpdateMeDep = Annotated[
    RedirectResponse,
    Depends(update_me),
]
UserDeleteMeDep = Annotated[
    RedirectResponse,
    Depends(delete_me),
]
UserGetAllDep = Annotated[
    Sequence[UserOutputDM],
    Depends(get_all_users),
]
UserGetDep = Annotated[
    UserOutputDM,
    Depends(get_user),
]
UserUpdateDep = Annotated[
    BaseResponse,
    Depends(update_user),
]
UserDeleteDep = Annotated[
    BaseResponse,
    Depends(delete_user),
]
