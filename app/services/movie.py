from abc import (
    abstractmethod,
)
from collections.abc import (
    Sequence,
)
from typing import (
    final,
    override,
)

import app.core.exceptions as exc
from app.api.v1.schemas import (
    MovieCreateDTO,
    MovieFilterDTO,
    MovieOutputDTO,
    MovieUpdateDTO,
)
from app.core.constants import (
    MESSAGE_MOVIE_NOT_FOUND,
)
from app.domains import (
    MovieFilterDM,
)
from app.services.base import (
    BaseService,
    BaseSqlAlchemyService,
)


class BaseMovieService(BaseService):
    @abstractmethod
    async def create_movie(
        self,
        movie_create: MovieCreateDTO,
    ) -> MovieOutputDTO:
        """Create a new movie.

        Parameters
        ----------
        movie_create : MovieCreateDTO
            movie data to create

        Returns
        -------
        MovieOutputDTO
            new movie data
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_movies(
        self,
        user_id: int,
        filters: MovieFilterDTO,
    ) -> Sequence[MovieOutputDTO]:
        """Get the user's filtered movies.

        Parameters
        ----------
        user_id : int
            relation user id

        filters : MovieFilterDTO
            movie search filter

        Returns
        -------
        Sequence[MovieOutputDTO]
            list of movies
        """
        raise NotImplementedError

    @abstractmethod
    async def get_movie(
        self,
        movie_id: int,
    ) -> MovieOutputDTO:
        """Get the movie by id.

        Parameters
        ----------
        movie_id : int
            movie id

        Returns
        -------
        MovieOutputDTO
            movie data

        Raises
        ------
        ResourceNotFoundError
            movie not found
        """
        raise NotImplementedError

    @abstractmethod
    async def update_movie(
        self,
        movie_id: int,
        movie_update: MovieUpdateDTO,
    ) -> MovieOutputDTO:
        """Update the movie by id.

        Parameters
        ----------
        movie_id : int
            movie id

        movie_update : MovieUpdateDTO
            movie data to update

        Returns
        -------
        MovieOutputDTO
            updated movie data

        Raises
        ------
        ResourceNotFoundError
            movie not found
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_movie(
        self,
        movie_id: int,
    ) -> MovieOutputDTO:
        """Delete the movie by id.

        Parameters
        ----------
        movie_id : int
            movie id

        Returns
        -------
        MovieOutputDTO
            movie data

        Raises
        ------
        ResourceNotFoundError
            movie not found
        """
        raise NotImplementedError


@final
class MovieService(BaseSqlAlchemyService, BaseMovieService):
    @override
    async def create_movie(
        self,
        movie_create: MovieCreateDTO,
    ) -> MovieOutputDTO:
        async with self.uow as uow:
            movie = await uow.movies.create(movie_create.model_dump())
            return MovieOutputDTO.model_validate(movie)

    @override
    async def get_all_movies(
        self,
        user_id: int,
        filters: MovieFilterDTO,
    ) -> Sequence[MovieOutputDTO]:
        async with self.uow as uow:
            movies = await uow.movies.read_all(
                filters=MovieFilterDM(
                    **filters.model_dump(),
                ),
                relation_id=user_id,
            )
            return [MovieOutputDTO.model_validate(movie) for movie in movies]

    @override
    async def get_movie(
        self,
        movie_id: int,
    ) -> MovieOutputDTO:
        async with self.uow as uow:
            movie = await uow.movies.read(movie_id)

            if movie is None:
                raise exc.ResourceNotFoundError(MESSAGE_MOVIE_NOT_FOUND)

            return MovieOutputDTO.model_validate(movie)

    @override
    async def update_movie(
        self,
        movie_id: int,
        movie_update: MovieUpdateDTO,
    ) -> MovieOutputDTO:
        async with self.uow as uow:
            movie = await uow.movies.update(
                item_id=movie_id,
                item_update=movie_update.model_dump(exclude_unset=True),
            )

            if movie is None:
                raise exc.ResourceNotFoundError(MESSAGE_MOVIE_NOT_FOUND)

            return MovieOutputDTO.model_validate(movie)

    @override
    async def delete_movie(
        self,
        movie_id: int,
    ) -> MovieOutputDTO:
        async with self.uow as uow:
            movie = await uow.movies.delete(movie_id)

            if movie is None:
                raise exc.ResourceNotFoundError(MESSAGE_MOVIE_NOT_FOUND)

            return MovieOutputDTO.model_validate(movie)
