from typing import final, override

from fastapi import Depends, params

import app.core.exceptions as exc
from app.api.v1.dependencies.base import BaseDependency
from app.domains import TypeUserRole, UserRole
from app.security import PayloadFromToken


@final
class _PermissionChecker(BaseDependency):
    """Verify user access rights based on role."""

    __slots__ = ("roles",)

    def __init__(
        self,
        *roles: TypeUserRole,
    ) -> None:
        """Initialize access verification.

        Parameters
        ----------
        roles : list[TypeUserRole]
            list of allowed roles
        """
        self.roles = set(roles) | {UserRole.admin}

    @override
    async def __call__(
        self,
        payload: PayloadFromToken,
    ) -> None:
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


def dep_permission_getter(
    *roles: TypeUserRole,
) -> params.Depends:
    """Get dependencies on permissions by roles.

    Parameters
    ----------
    roles : list[TypeUserRole]
        list of allowed roles

    Returns
    -------
    Depends
        dependency on permissions
    """
    return Depends(_PermissionChecker(*roles))
