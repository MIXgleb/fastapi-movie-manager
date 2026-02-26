from typing import (
    final,
    override,
)

from fastapi import (
    Depends,
    params,
)

import app.core.exceptions as exc
from app.api.v1.dependencies.security.base import (
    BaseDependency,
)
from app.domains import (
    UserRole,
)
from app.security.auth_managers import (
    PayloadDep,
)


@final
class PermissionChecker(BaseDependency):
    """Verifying user access rights."""

    __slots__ = ("roles",)

    def __init__(
        self,
        *roles: UserRole,
    ) -> None:
        """
        Initialize access verification.

        Parameters
        ----------
        *roles : UserRole
            allowed roles
        """
        self.roles = set(roles) | {UserRole.ADMIN}

    @override
    async def __call__(
        self,
        payload: PayloadDep,
    ) -> None:
        """
        Check a user's permissions.

        Parameters
        ----------
        payload : PayloadDep
            payload data

        Raises
        ------
        UserPermissionError
            access is forbidden
        """
        if payload.user_role not in self.roles:
            raise exc.UserPermissionError


def dep_permission_getter(
    *roles: UserRole,
) -> params.Depends:
    """
    Get dependency on permissions by roles.

    Parameters
    ----------
    *roles : UserRole
        allowed roles

    Returns
    -------
    Depends
        dependency on permissions
    """
    return Depends(
        dependency=PermissionChecker(*roles),
    )
