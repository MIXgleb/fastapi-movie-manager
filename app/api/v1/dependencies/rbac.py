from typing import final, override

from fastapi import Depends, params

from app.api.v1.dependencies.base import EndpointDependencyBase, PayloadByToken
from app.core import exceptions as exc
from app.domains import UserRole, UserRoleType


@final
class _PermissionChecker(EndpointDependencyBase):
    """Verify user access rights based on role."""

    __slots__ = ("roles",)

    def __init__(self, *roles: UserRoleType) -> None:
        """Initialize access verification.

        Parameters
        ----------
        roles : list[UserRoleType]
            list of allowed roles
        """
        self.roles = set(roles) | {UserRole.admin}

    @override
    async def __call__(self, payload: PayloadByToken) -> None:
        """Check the user's permissions.

        Parameters
        ----------
        payload : Payload
            payload data

        Raises
        ------
        UserPermissionError
            access is forbidden
        """
        if payload.user_role not in self.roles:
            raise exc.UserPermissionError


def dep_permission_getter(*roles: UserRoleType) -> params.Depends:
    """Get dependencies on permissions by roles.

    Parameters
    ----------
    roles : list[UserRoleType]
        list of allowed roles

    Returns
    -------
    Depends
        dependency on permissions
    """
    return Depends(_PermissionChecker(*roles))
