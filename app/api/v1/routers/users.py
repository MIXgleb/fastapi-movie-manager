from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.api.v1.deps import PermissionChecker, UserOwnershipChecker
from app.api.v1.schemas import MessageDeleteUserReturn
from app.core.config import settings
from app.core.security import TokenHelper
from app.schemas import Payload, Role, UserFilters, UserOutput
from app.services import SqlAlchemyServiceHelper, UserService, UserServiceBase

router = APIRouter(prefix=settings.api.v1.users, tags=["Users"])
user_service_helper = SqlAlchemyServiceHelper(UserService)


@router.get("/me", response_model=UserOutput)
async def get_me(
    user_service: Annotated[UserServiceBase, Depends(user_service_helper.service_getter)],
    payload: Annotated[Payload, Depends(TokenHelper())],
):
    """Get my user's information.

    Parameters
    ----------
    user_service : UserServiceBase
        user service

    payload : Payload
        payload data

    Returns
    -------
    UserOutput
        user data
    """
    if payload.user_id == 0:
        return UserOutput(
            username="guest",
            id=payload.user_id,
            role=payload.user_role,
            created_at=datetime.now(UTC),
        )
    return await user_service.get_user(payload.user_id)


@router.get(
    "/all",
    response_model=list[UserOutput],
    dependencies=[Depends(PermissionChecker(Role.admin))],
)
async def get_all_users(
    user_service: Annotated[UserServiceBase, Depends(user_service_helper.service_getter)],
    filters: Annotated[UserFilters, Query()],
):
    """Get all users.

    Parameters
    ----------
    user_service : UserServiceBase
        user service

    filters : UserFilters
        user search filter

    Returns
    -------
    list[UserOutput]
        data of users
    """
    return await user_service.get_all_users(filters)


@router.get(
    "/{user_id}",
    response_model=UserOutput,
    dependencies=[
        Depends(PermissionChecker(Role.admin, Role.user)),
        Depends(UserOwnershipChecker()),
    ],
)
async def get_user(
    user_service: Annotated[UserServiceBase, Depends(user_service_helper.service_getter)],
    user_id: Annotated[int, Path()],
):
    """Get user's information by id.

    Parameters
    ----------
    user_service : UserServiceBase
        user service

    user_id : int
        user id

    Returns
    -------
    UserOutput
        user data
    """
    return await user_service.get_user(user_id)


@router.delete(
    "/{user_id}",
    response_model=MessageDeleteUserReturn,
    dependencies=[
        Depends(PermissionChecker(Role.admin, Role.user)),
        Depends(UserOwnershipChecker()),
    ],
)
async def delete_user(
    user_service: Annotated[UserServiceBase, Depends(user_service_helper.service_getter)],
    user_id: Annotated[int, Path()],
):
    """Delete user by id.

    Parameters
    ----------
    user_service : UserServiceBase
        user service

    user_id : int
        user id

    Returns
    -------
    MessageDeleteUserReturn
        status message
    """
    user = await user_service.delete_user(user_id)
    user_output = UserOutput.model_validate(user, from_attributes=True)
    return MessageDeleteUserReturn(user=user_output)
