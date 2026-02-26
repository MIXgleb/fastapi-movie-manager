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
from app.services import (
    MovieService,
)
from app.services.service_managers import (
    SqlAlchemyServiceManager,
)

MovieIdFromPath = Annotated[int | UUID, Path()]


@final
class MovieOwnershipChecker(BaseDependency):
    """Verifying a user's ownership of a movie."""

    __slots__ = ("service_manager",)

    def __init__(
        self,
        service_manager: SqlAlchemyServiceManager[MovieService],
    ) -> None:
        """
        Initialize resource ownership verification.

        Parameters
        ----------
        service_manager : SqlAlchemyServiceManager
            movie service manager
        """
        self.service_manager = service_manager

    @override
    async def __call__(
        self,
        movie_id: MovieIdFromPath,
        payload: PayloadDep,
        request: Request,
    ) -> None:
        """
        Check a user's ownership rights.

        Parameters
        ----------
        movie_id : MovieIdFromPath
            movie id

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
        movie = await self.service_manager.service.get_movie(movie_id)

        if method == "POST":
            raise exc.IncorrectMethodError

        if method == "GET" and (is_admin or movie.user_id == payload.user_id):
            return

        if method in {"PUT", "DELETE"} and (is_admin or movie.user_id == payload.user_id):
            return

        raise exc.ResourceOwnershipError


def dep_movie_ownership_getter(
    service_manager: SqlAlchemyServiceManager[MovieService],
) -> params.Depends:
    """
    Get dependency on resource ownership.

    Parameters
    ----------
    service_manager : SqlAlchemyServiceManager
        movie service manager

    Returns
    -------
    Depends
        dependency on ownership
    """
    return Depends(
        dependency=MovieOwnershipChecker(
            service_manager=service_manager,
        ),
    )
