from abc import (
    abstractmethod,
)
from collections.abc import (
    Sequence,
)
from typing import (
    Final,
    final,
    override,
)
from uuid import (
    UUID,
)

import app.core.exceptions as exc
from app.domains import (
    MovieCreateDM,
    MovieFiltersDM,
    MovieInputDM,
    MovieOutputDM,
    MovieUpdateDM,
)
from app.services.base import (
    BaseService,
    BaseSqlAlchemyService,
)

MovieNotFoundError: Final[Exception] = exc.ResourceNotFoundError("Movie not found.")


class BaseMovieService(BaseService):
    """Basic abstract movie service class."""

    @abstractmethod
    async def create_movie(
        self,
        movie_input: MovieInputDM,
        user_id: UUID,
    ) -> MovieOutputDM:
        """
        Create a new movie.

        Parameters
        ----------
        movie_input : MovieInputDM
            movie data to create

        user_id : UUID
            user id

        Returns
        -------
        MovieOutputDM
            new movie data
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_movies(
        self,
        user_id: UUID,
        filters: MovieFiltersDM,
    ) -> Sequence[MovieOutputDM]:
        """
        Get a user's filtered movies.

        Parameters
        ----------
        user_id : UUID
            relation user id

        filters : MovieFiltersDM
            movie search filter

        Returns
        -------
        Sequence[MovieOutputDM]
            list of movies
        """
        raise NotImplementedError

    @abstractmethod
    async def get_movie(
        self,
        movie_id: int | UUID,
    ) -> MovieOutputDM:
        """
        Get a movie by id.

        Parameters
        ----------
        movie_id : int | UUID
            movie id

        Returns
        -------
        MovieOutputDM
            movie data

        Raises
        ------
        MovieNotFoundError
            movie not found
        """
        raise NotImplementedError

    @abstractmethod
    async def update_movie(
        self,
        movie_id: int | UUID,
        movie_update: MovieUpdateDM,
    ) -> MovieOutputDM:
        """
        Update a movie by id.

        Parameters
        ----------
        movie_id : int | UUID
            movie id

        movie_update : MovieUpdateDM
            movie data to update

        Returns
        -------
        MovieOutputDM
            updated movie data

        Raises
        ------
        MovieNotFoundError
            movie not found
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_movie(
        self,
        movie_id: int | UUID,
    ) -> MovieOutputDM:
        """
        Delete a movie by id.

        Parameters
        ----------
        movie_id : int | UUID
            movie id

        Returns
        -------
        MovieOutputDM
            movie data

        Raises
        ------
        MovieNotFoundError
            movie not found
        """
        raise NotImplementedError


@final
class MovieService(
    BaseSqlAlchemyService,
    BaseMovieService,
):
    """SqlAlchemy movie service."""

    @override
    async def create_movie(
        self,
        movie_input: MovieInputDM,
        user_id: UUID,
    ) -> MovieOutputDM:
        movie_create = MovieCreateDM.from_object(
            movie_input,
            none_if_key_not_found=True,
            user_id=user_id,
        )

        async with self.uow as uow:
            movie = await uow.movies.create(movie_create)
            return MovieOutputDM.from_object(movie)

    @override
    async def get_all_movies(
        self,
        user_id: UUID,
        filters: MovieFiltersDM,
    ) -> Sequence[MovieOutputDM]:
        async with self.uow as uow:
            movies = await uow.movies.read_all(
                filters=filters,
                relation_id=user_id,
            )
            return [MovieOutputDM.from_object(movie) for movie in movies]

    @override
    async def get_movie(
        self,
        movie_id: int | UUID,
    ) -> MovieOutputDM:
        async with self.uow as uow:
            movie = await uow.movies.read(movie_id)

            if movie is None:
                raise MovieNotFoundError

            return MovieOutputDM.from_object(movie)

    @override
    async def update_movie(
        self,
        movie_id: int | UUID,
        movie_update: MovieUpdateDM,
    ) -> MovieOutputDM:
        async with self.uow as uow:
            movie = await uow.movies.update(
                item_id=movie_id,
                item_update=movie_update,
            )

            if movie is None:
                raise MovieNotFoundError

            return MovieOutputDM.from_object(movie)

    @override
    async def delete_movie(
        self,
        movie_id: int | UUID,
    ) -> MovieOutputDM:
        async with self.uow as uow:
            movie = await uow.movies.delete(movie_id)

            if movie is None:
                raise MovieNotFoundError

            return MovieOutputDM.from_object(movie)
