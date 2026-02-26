from collections.abc import (
    Sequence,
)
from typing import (
    Annotated,
)
from uuid import (
    UUID,
)

from fastapi import (
    Body,
    Depends,
    Path,
    Query,
)

from app.api.v1.dependencies.security import (
    dep_movie_ownership_getter,
)
from app.api.v1.schemas import (
    BaseResponse,
    MovieFilterDTO,
    MovieInputDTO,
    MovieOutputDTO,
    MovieUpdateDTO,
    ResponseDeleteMovie,
    ResponseUpdateMovie,
)
from app.domains import (
    MovieFiltersDM,
    MovieInputDM,
    MovieOutputDM,
    MovieUpdateDM,
)
from app.security.auth_managers import (
    PayloadDep,
)
from app.services import (
    BaseMovieService,
    MovieService,
)
from app.services.service_managers import (
    SqlAlchemyServiceManager,
)

movie_service_manager = SqlAlchemyServiceManager(
    service_class=MovieService,
)

MovieServiceDep = Annotated[
    BaseMovieService,
    Depends(movie_service_manager.service_getter),
]
MovieFromBody = Annotated[MovieInputDTO, Body()]
MovieIdFromPath = Annotated[int | UUID, Path()]
MovieFilterFromQuery = Annotated[MovieFilterDTO, Query()]
MovieUpdateFromBody = Annotated[MovieUpdateDTO, Body()]


async def create_movie(
    movie_service: MovieServiceDep,
    payload: PayloadDep,
    movie_input: MovieFromBody,
) -> MovieOutputDM:
    """
    Create a new movie.

    Parameters
    ----------
    movie_service : MovieServiceDep
        movie service

    payload : PayloadDep
        payload data

    movie_input : MovieFromBody
        new movie data

    Returns
    -------
    MovieOutputDM
        movie data
    """
    return await movie_service.create_movie(
        movie_input=MovieInputDM.from_object(movie_input),
        user_id=payload.user_id,
    )


async def get_all_movies(
    movie_service: MovieServiceDep,
    payload: PayloadDep,
    filters: MovieFilterFromQuery,
) -> Sequence[MovieOutputDM]:
    """
    Get all user's movies.

    Parameters
    ----------
    movie_service : MovieServiceDep
        movie service

    payload : PayloadDep
        payload data

    filters : MovieFilterFromQuery
        movie search filter

    Returns
    -------
    Sequence[MovieOutputDM]
        data of movies
    """
    return await movie_service.get_all_movies(
        user_id=payload.user_id,
        filters=MovieFiltersDM.from_object(filters),
    )


async def get_movie(
    movie_service: MovieServiceDep,
    movie_id: MovieIdFromPath,
) -> MovieOutputDM:
    """
    Get a movie by id.

    Parameters
    ----------
    movie_service : MovieServiceDep
        movie service

    movie_id : MovieIdFromPath
        movie id

    Returns
    -------
    MovieOutputDM
        movie data
    """
    return await movie_service.get_movie(
        movie_id=movie_id,
    )


async def update_movie(
    movie_service: MovieServiceDep,
    movie_id: MovieIdFromPath,
    movie_update: MovieUpdateFromBody,
) -> BaseResponse:
    """
    Update a movie by id.

    Parameters
    ----------
    movie_service : MovieServiceDep
        movie service

    movie_id : MovieIdFromPath
        movie id

    movie_update : MovieUpdateFromBody
        movie data to update

    Returns
    -------
    BaseResponse
        status message
    """
    movie = await movie_service.update_movie(
        movie_id=movie_id,
        movie_update=MovieUpdateDM.from_object(
            movie_update.model_dump(exclude_unset=True),
            none_if_key_not_found=True,
        ),
    )
    return ResponseUpdateMovie(
        movie=MovieOutputDTO.model_validate(movie),
    )


async def delete_movie(
    movie_service: MovieServiceDep,
    movie_id: MovieIdFromPath,
) -> BaseResponse:
    """
    Delete a movie by id.

    Parameters
    ----------
    movie_service : MovieServiceDep
        movie service

    movie_id : MovieIdFromPath
        movie id

    Returns
    -------
    BaseResponse
        status message
    """
    movie = await movie_service.delete_movie(
        movie_id=movie_id,
    )
    return ResponseDeleteMovie(
        movie=MovieOutputDTO.model_validate(movie),
    )


MovieOwnershipDep = dep_movie_ownership_getter(
    service_manager=movie_service_manager,
)
MovieCreateDep = Annotated[
    MovieOutputDM,
    Depends(create_movie),
]
MovieGetAllDep = Annotated[
    Sequence[MovieOutputDM],
    Depends(get_all_movies),
]
MovieGetDep = Annotated[
    MovieOutputDM,
    Depends(get_movie),
]
MovieUpdateDep = Annotated[
    BaseResponse,
    Depends(update_movie),
]
MovieDeleteDep = Annotated[
    BaseResponse,
    Depends(delete_movie),
]
