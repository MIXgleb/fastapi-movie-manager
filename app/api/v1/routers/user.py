from collections.abc import (
    Sequence,
)

from fastapi import (
    APIRouter,
)
from fastapi.responses import (
    RedirectResponse,
)

from app.api.v1.dependencies import (
    UserDeleteDep,
    UserDeleteMeDep,
    UserGetAllDep,
    UserGetDep,
    UserGetMeDep,
    UserOwnershipDep,
    UserUpdateDep,
    UserUpdateMeDep,
    dep_permission_getter,
)
from app.api.v1.schemas import (
    BaseResponse,
    ResponseDeleteUser,
    ResponseUpdateUser,
    UserOutputDTO,
)
from app.core import (
    dep_rate_limiter_getter,
    settings,
)
from app.domains import (
    UserOutputDM,
    UserRole,
)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
    dependencies=[
        dep_rate_limiter_getter(seconds=2, limit=2),
    ],
)


@router.get(
    path="/me",
)
async def get_me(
    user: UserGetMeDep,
) -> RedirectResponse:
    """
    Get my user's information.

    Parameters
    ----------
    user : UserGetMeDep
        user data

    Returns
    -------
    RedirectResponse
        redirect response (308)
    """
    return user


@router.put(
    path="/me",
)
async def update_me(
    updated_user: UserUpdateMeDep,
) -> RedirectResponse:
    """
    Update my user's information.

    Parameters
    ----------
    updated_user : UserUpdateMeDep
        updated user data

    Returns
    -------
    RedirectResponse
        redirect response (308)
    """
    return updated_user


@router.delete(
    path="/me",
)
async def delete_me(
    deleted_user: UserDeleteMeDep,
) -> RedirectResponse:
    """
    Delete my account.

    Parameters
    ----------
    deleted_user : UserDeleteMeDep
        deleted user data

    Returns
    -------
    RedirectResponse
        redirect response (308)
    """
    return deleted_user


@router.get(
    path="/all",
    response_model=list[UserOutputDTO],
    dependencies=[
        dep_permission_getter(
            UserRole.ADMIN,
        ),
    ],
)
async def get_all_users(
    users: UserGetAllDep,
) -> Sequence[UserOutputDM]:
    """
    Get all users.

    Parameters
    ----------
    users : UserGetAllDep
        data of users

    Returns
    -------
    Sequence[UserOutputDM]
        data of users
    """
    return users


@router.get(
    path="/{user_id}",
    response_model=UserOutputDTO,
    dependencies=[
        UserOwnershipDep,
    ],
)
async def get_user(
    user: UserGetDep,
) -> UserOutputDM:
    """
    Get user's information by id.

    Parameters
    ----------
    user : UserGetDep
        user data

    Returns
    -------
    UserOutputDM
        user data
    """
    return user


@router.put(
    path="/{user_id}",
    response_model=ResponseUpdateUser,
    dependencies=[
        dep_permission_getter(
            UserRole.ADMIN,
            UserRole.USER,
        ),
        UserOwnershipDep,
    ],
)
async def update_user(
    updated_user: UserUpdateDep,
) -> BaseResponse:
    """
    Update a user by id.

    Parameters
    ----------
    updated_user : UserUpdateDep
        updated user data

    Returns
    -------
    BaseResponse
        status message
    """
    return updated_user


@router.delete(
    path="/{user_id}",
    response_model=ResponseDeleteUser,
    dependencies=[
        dep_permission_getter(
            UserRole.ADMIN,
            UserRole.USER,
        ),
        UserOwnershipDep,
    ],
)
async def delete_user(
    deleted_user: UserDeleteDep,
) -> BaseResponse:
    """
    Delete user by id.

    Parameters
    ----------
    deleted_user : UserDeleteDep
        deleted user data

    Returns
    -------
    BaseResponse
        status message
    """
    return deleted_user
