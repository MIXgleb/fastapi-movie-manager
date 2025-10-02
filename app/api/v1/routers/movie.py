from collections.abc import Sequence
from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Path,
    Query,
    status,
)
from fastapi_limiter.depends import RateLimiter

from app.api.v1.dependencies import (
    PayloadByToken,
    dep_movie_ownership_getter,
    dep_permission_getter,
)
from app.api.v1.schemas import (
    DeleteMovieResponse,
    MovieCreateDTO,
    MovieFilterDTO,
    MovieInputDTO,
    MovieOutputDTO,
    MovieUpdateDTO,
    UpdateMovieResponse,
)
from app.core.config import settings
from app.domains import UserRole
from app.services import (
    MovieService,
    MovieServiceBase,
    SqlAlchemyServiceHelper,
)

router = APIRouter(
    prefix=settings.api.v1.movies,
    tags=["Movies"],
    dependencies=[Depends(RateLimiter(seconds=1))],
)
movie_service_helper = SqlAlchemyServiceHelper(MovieService)
MovieOwnership = dep_movie_ownership_getter(movie_service_helper)

MovieServiceType = Annotated[
    MovieServiceBase,
    Depends(movie_service_helper.service_getter),
]
MovieFromBody = Annotated[MovieInputDTO, Body()]
MovieIdFromPath = Annotated[int, Path()]
MovieFilterFromQuery = Annotated[MovieFilterDTO, Query()]
MovieUpdateFromBody = Annotated[MovieUpdateDTO, Body()]


@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    dependencies=[dep_permission_getter(UserRole.admin, UserRole.user)],
)
async def create_movie(
    movie_service: MovieServiceType,
    payload: PayloadByToken,
    movie_input: MovieFromBody,
) -> MovieOutputDTO:
    """Create a new movie.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    payload : Payload
        payload data

    movie_input : MovieInputDTO
        new movie data

    Returns
    -------
    MovieOutputDTO
        movie data
    """
    movie_create = MovieCreateDTO(**movie_input.model_dump(), user_id=payload.user_id)
    return await movie_service.create_movie(movie_create)


@router.get(
    "/all",
    dependencies=[dep_permission_getter(UserRole.admin, UserRole.user)],
)
async def get_all_movies(
    movie_service: MovieServiceType,
    payload: PayloadByToken,
    filters: MovieFilterFromQuery,
) -> Sequence[MovieOutputDTO]:
    """Get all the user's movies.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    payload : Payload
        payload data

    filters : MovieFilterDTO
        movie search filter

    Returns
    -------
    Sequence[MovieOutputDTO]
        data of movies
    """
    return await movie_service.get_all_movies(payload.user_id, filters)


@router.get(
    "/{movie_id}",
    dependencies=[MovieOwnership],
)
async def get_movie(
    movie_service: MovieServiceType,
    movie_id: MovieIdFromPath,
) -> MovieOutputDTO:
    """Get the movie by id.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    movie_id : int
        movie id

    Returns
    -------
    MovieOutputDTO
        movie data
    """
    return await movie_service.get_movie(movie_id)


@router.put(
    "/{movie_id}",
    dependencies=[
        dep_permission_getter(UserRole.admin, UserRole.user),
        MovieOwnership,
    ],
)
async def update_movie(
    movie_service: MovieServiceType,
    movie_id: MovieIdFromPath,
    movie_update: MovieUpdateFromBody,
) -> UpdateMovieResponse:
    """Update the movie by id.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    movie_id : int
        movie id

    movie_update : MovieUpdateDTO
        movie data to update

    Returns
    -------
    UpdateMovieResponse
        status message
    """
    movie = await movie_service.update_movie(movie_id, movie_update)
    return UpdateMovieResponse(movie=movie)


@router.delete(
    "/{movie_id}",
    dependencies=[
        dep_permission_getter(UserRole.admin, UserRole.user),
        MovieOwnership,
    ],
)
async def delete_movie(
    movie_service: MovieServiceType,
    movie_id: MovieIdFromPath,
) -> DeleteMovieResponse:
    """Delete the movie by id.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    movie_id : int
        movie id

    Returns
    -------
    DeleteMovieResponse
        status message
    """
    movie = await movie_service.delete_movie(movie_id)
    return DeleteMovieResponse(movie=movie)
