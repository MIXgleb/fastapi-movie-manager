from typing import (
    Annotated,
    final,
    override,
)

from fastapi import (
    Depends,
    Path,
    Request,
    params,
)

import app.core.exceptions as exc
from app.api.v1.dependencies.base import (
    BaseDependency,
)
from app.domains import (
    UserRole,
)
from app.security import (
    PayloadFromToken,
)
from app.services import (
    MovieService,
    SqlAlchemyServiceHelper,
)

UserIdFromPath = Annotated[int, Path()]


@final
class _UserOwnershipChecker(BaseDependency):
    """Verifying the user's ownership of a resource."""

    @override
    async def __call__(
        self,
        user_id: UserIdFromPath,
        payload: PayloadFromToken,
        request: Request,
    ) -> None:
        """Check the user's ownership rights.

        Parameters
        ----------
        user_id : int
            user id

        payload : Payload
            payload data

        request : Request
            request from the client

        Raises
        ------
        WrondMethodError
            method not allowed

        ResourceOwnershipError
            access is forbidden
        """
        method = request.method
        is_admin = payload.user_role == UserRole.admin

        if method == "POST":
            raise exc.WrondMethodError

        if method in {"GET", "PUT", "DELETE"} and (is_admin or user_id == payload.user_id):
            return

        raise exc.ResourceOwnershipError


UserOwnership = Depends(_UserOwnershipChecker())


@final
class _MovieOwnershipChecker(BaseDependency):
    """Verifying the user's ownership of a movie."""

    __slots__ = ("service_helper",)

    def __init__(
        self,
        service_helper: SqlAlchemyServiceHelper[MovieService],
    ) -> None:
        """Initialize resource ownership verification.

        Parameters
        ----------
        service_helper : SqlAlchemyServiceHelper
            movie service helper
        """
        self.service_helper = service_helper

    @override
    async def __call__(
        self,
        movie_id: UserIdFromPath,
        payload: PayloadFromToken,
        request: Request,
    ) -> None:
        """Check the user's ownership rights.

        Parameters
        ----------
        movie_id : int
            movie id

        payload : Payload
            payload data

        request : Request
            request from the client

        Raises
        ------
        WrondMethodError
            method not allowed

        ResourceOwnershipError
            access is forbidden
        """
        method = request.method
        is_admin = payload.user_role == UserRole.admin
        movie = await self.service_helper.service.get_movie(movie_id)

        if method == "POST":
            raise exc.WrondMethodError

        if method == "GET" and (is_admin or movie.user_id == payload.user_id):
            return

        if method in {"PUT", "DELETE"} and (is_admin or movie.user_id == payload.user_id):
            return

        raise exc.ResourceOwnershipError


def dep_movie_ownership_getter(
    service_helper: SqlAlchemyServiceHelper[MovieService],
) -> params.Depends:
    """Get dependencies on resource ownership.

    Parameters
    ----------
    service_helper : SqlAlchemyServiceHelper
        movie service helper

    Returns
    -------
    Depends
        dependency on ownership
    """
    return Depends(_MovieOwnershipChecker(service_helper))
