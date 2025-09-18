from typing import Annotated, final, override

from fastapi import Depends

from app.api.v1.deps.base import EndpointDependencyBase
from app.core import exceptions as exc
from app.core.security import TokenHelper
from app.schemas import USER_ROLES, Payload, Role


@final
class PermissionChecker(EndpointDependencyBase):
    """Verify user access rights based on role."""

    __slots__ = ("roles",)

    def __init__(self, *roles: USER_ROLES) -> None:
        """Initialize access verification.

        Parameters
        ----------
        roles : list[USER_ROLES]
            list of allowed roles
        """
        self.roles = set(roles) | {Role.admin}

    @override
    async def __call__(self, payload: Annotated[Payload, Depends(TokenHelper())]) -> None:
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
