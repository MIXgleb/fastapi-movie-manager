from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query

from app.api.v1.deps import MovieOwnershipChecker, PermissionChecker
from app.api.v1.schemas import MessageDeleteMovieReturn, MessageUpdateMovieReturn
from app.core.config import settings
from app.core.security import TokenHelper
from app.schemas import MovieFilters, MovieInput, MovieOutput, MovieUpdate, Payload, Role
from app.services import MovieService, MovieServiceBase, SqlAlchemyServiceHelper

router = APIRouter(prefix=settings.api.v1.movies, tags=["Movies"])
movie_service_helper = SqlAlchemyServiceHelper(MovieService)


@router.post(
    "/new",
    response_model=MovieOutput,
    dependencies=[Depends(PermissionChecker(Role.admin, Role.user))],
)
async def create_movie(
    movie_service: Annotated[MovieServiceBase, Depends(movie_service_helper.service_getter)],
    payload: Annotated[Payload, Depends(TokenHelper())],
    movie_input: Annotated[MovieInput, Body()],
):
    """Create a new movie.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    payload : Payload
        payload data

    movie_input : MovieInput
        new movie data

    Returns
    -------
    MovieOutput
        movie data
    """
    return await movie_service.create_movie(movie_input, payload.user_id)


@router.get(
    "/all",
    response_model=list[MovieOutput],
    dependencies=[Depends(PermissionChecker(Role.admin, Role.user))],
)
async def get_all_movies(
    movie_service: Annotated[MovieServiceBase, Depends(movie_service_helper.service_getter)],
    payload: Annotated[Payload, Depends(TokenHelper())],
    filters: Annotated[MovieFilters, Query()],
):
    """Get all the user's movies.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    payload : Payload
        payload data

    filters : MovieFilters
        movie search filter

    Returns
    -------
    list[MovieOutput]
        data of movies
    """
    return await movie_service.get_all_movies(filters, payload.user_id)


@router.get(
    "/{movie_id}",
    response_model=MovieOutput,
    dependencies=[Depends(MovieOwnershipChecker(movie_service_helper))],
)
async def get_movie(
    movie_service: Annotated[MovieServiceBase, Depends(movie_service_helper.service_getter)],
    movie_id: Annotated[int, Path()],
):
    """Get the movie by id.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    movie_id : int
        movie id

    Returns
    -------
    MovieOutput
        movie data
    """
    return await movie_service.get_movie(movie_id)


@router.put(
    "/{movie_id}",
    response_model=MessageUpdateMovieReturn,
    dependencies=[
        Depends(PermissionChecker(Role.admin, Role.user)),
        Depends(MovieOwnershipChecker(movie_service_helper)),
    ],
)
async def update_movie(
    movie_service: Annotated[MovieServiceBase, Depends(movie_service_helper.service_getter)],
    movie_id: Annotated[int, Path()],
    movie_update: Annotated[MovieUpdate, Body()],
):
    """Update the movie by id.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    movie_id : int
        movie id

    movie_update : MovieUpdate
        movie data to update

    Returns
    -------
    MessageUpdateMovieReturn
        status message
    """
    movie = await movie_service.update_movie(movie_update, movie_id)
    movie_output = MovieOutput.model_validate(movie, from_attributes=True)
    return MessageUpdateMovieReturn(movie=movie_output)


@router.delete(
    "/{movie_id}",
    response_model=MessageDeleteMovieReturn,
    dependencies=[
        Depends(PermissionChecker(Role.admin, Role.user)),
        Depends(MovieOwnershipChecker(movie_service_helper)),
    ],
)
async def delete_movie(
    movie_service: Annotated[MovieServiceBase, Depends(movie_service_helper.service_getter)],
    movie_id: Annotated[int, Path()],
):
    """Delete the movie by id.

    Parameters
    ----------
    movie_service : MovieServiceBase
        movie service

    movie_id : int
        movie id

    Returns
    -------
    MessageDeleteMovieReturn
        status message
    """
    movie = await movie_service.delete_movie(movie_id)
    movie_output = MovieOutput.model_validate(movie, from_attributes=True)
    return MessageDeleteMovieReturn(movie=movie_output)
