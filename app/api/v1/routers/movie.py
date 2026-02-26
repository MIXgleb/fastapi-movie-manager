from collections.abc import (
    Sequence,
)

from fastapi import (
    APIRouter,
    status,
)

from app.api.v1.dependencies import (
    MovieCreateDep,
    MovieDeleteDep,
    MovieGetAllDep,
    MovieGetDep,
    MovieOwnershipDep,
    MovieUpdateDep,
    dep_permission_getter,
)
from app.api.v1.schemas import (
    BaseResponse,
    MovieOutputDTO,
    ResponseDeleteMovie,
    ResponseUpdateMovie,
)
from app.core import (
    dep_rate_limiter_getter,
    settings,
)
from app.domains import (
    MovieOutputDM,
    UserRole,
)

router = APIRouter(
    prefix=settings.api.v1.movies,
    tags=["Movies"],
    dependencies=[
        dep_rate_limiter_getter(seconds=1),
    ],
)


@router.post(
    path="/new",
    response_model=MovieOutputDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        dep_permission_getter(
            UserRole.ADMIN,
            UserRole.USER,
        ),
    ],
)
async def create_movie(
    created_movie: MovieCreateDep,
) -> MovieOutputDM:
    """
    Create a new movie.

    Parameters
    ----------
    created_movie : MovieCreateDep
        created movie data

    Returns
    -------
    MovieOutputDM
        movie data
    """
    return created_movie


@router.get(
    path="/all",
    response_model=list[MovieOutputDTO],
    dependencies=[
        dep_permission_getter(
            UserRole.ADMIN,
            UserRole.USER,
        ),
    ],
)
async def get_all_movies(
    movies: MovieGetAllDep,
) -> Sequence[MovieOutputDM]:
    """
    Get all user's movies.

    Parameters
    ----------
    movies : MovieGetAllDep
        user's movies

    Returns
    -------
    Sequence[MovieOutputDM]
        data of movies
    """
    return movies


@router.get(
    path="/{movie_id}",
    response_model=MovieOutputDTO,
)
async def get_movie(
    movie: MovieGetDep,
) -> MovieOutputDM:
    """
    Get a movie by id.

    Parameters
    ----------
    movie : MovieGetDep
        found movie data

    Returns
    -------
    MovieOutputDM
        movie data
    """
    return movie


@router.put(
    path="/{movie_id}",
    response_model=ResponseUpdateMovie,
    dependencies=[
        dep_permission_getter(
            UserRole.ADMIN,
            UserRole.USER,
        ),
        MovieOwnershipDep,
    ],
)
async def update_movie(
    updated_movie: MovieUpdateDep,
) -> BaseResponse:
    """
    Update a movie by id.

    Parameters
    ----------
    updated_movie : MovieUpdateDep
        updated movie data

    Returns
    -------
    BaseResponse
        status message
    """
    return updated_movie


@router.delete(
    path="/{movie_id}",
    response_model=ResponseDeleteMovie,
    dependencies=[
        dep_permission_getter(
            UserRole.ADMIN,
            UserRole.USER,
        ),
        MovieOwnershipDep,
    ],
)
async def delete_movie(
    deleted_movie: MovieDeleteDep,
) -> BaseResponse:
    """
    Delete a movie by id.

    Parameters
    ----------
    deleted_movie : MovieDeleteDep
        deleted movie data

    Returns
    -------
    BaseResponse
        status message
    """
    return deleted_movie
