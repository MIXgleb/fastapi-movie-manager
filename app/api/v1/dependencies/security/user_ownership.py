from typing import (
    Annotated,
    final,
    override,
)
from uuid import (
    UUID,
)

from fastapi import (
    Depends,
    Path,
    Request,
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

UserIdFromPath = Annotated[UUID, Path()]


@final
class UserOwnershipChecker(BaseDependency):
    """Verifying a user's ownership."""

    @override
    async def __call__(
        self,
        user_id: UserIdFromPath,
        payload: PayloadDep,
        request: Request,
    ) -> None:
        """
        Check a user's ownership rights.

        Parameters
        ----------
        user_id : UserIdFromPath
            user id

        payload : PayloadDep
            payload data

        request : Request
            request from the client

        Raises
        ------
        IncorrectMethodError
            method not allowed

        ResourceOwnershipError
            access is forbidden
        """
        method = request.method
        is_admin = payload.user_role is UserRole.ADMIN

        if method == "POST":
            raise exc.IncorrectMethodError

        if method in {"GET", "PUT", "DELETE"} and (is_admin or user_id == payload.user_id):
            return

        raise exc.ResourceOwnershipError


def dep_user_ownership_getter() -> params.Depends:
    """
    Get dependency on resource ownership.

    Returns
    -------
    Depends
        dependency on ownership
    """
    return Depends(
        dependency=UserOwnershipChecker(),
    )
