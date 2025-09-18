from abc import abstractmethod
from collections.abc import Sequence
from typing import Final, final, override

import app.core.exceptions as exc
from app.database.models import Movie
from app.schemas import MovieCreate, MovieFilters, MovieInput, MovieUpdate
from app.services.base import ServiceBase, SqlAlchemyServiceBase

MSG_MOVIE_NOT_FOUND: Final[str] = "Movie not found."


class MovieServiceBase(ServiceBase):
    @abstractmethod
    async def create_movie(self, movie_create: MovieInput, user_id: int) -> Movie:
        """Create a new movie.

        Parameters
        ----------
        movie_create : MovieInput
            new movie data

        user_id : int
            movie user id

        Returns
        -------
        Movie
            new movie data
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_movies(self, filters: MovieFilters, user_id: int) -> Sequence[Movie]:
        """Get the user's filtered movies.

        Parameters
        ----------
        filters : MovieFilters
            movie search filter

        user_id : int
            relation user id

        Returns
        -------
        Sequence[Movie]
            list of movies
        """
        raise NotImplementedError

    @abstractmethod
    async def get_movie(self, movie_id: int) -> Movie:
        """Get the movie by id.

        Parameters
        ----------
        movie_id : int
            movie id

        Returns
        -------
        Movie
            movie data
        """
        raise NotImplementedError

    @abstractmethod
    async def update_movie(self, movie_update: MovieUpdate, movie_id: int) -> Movie:
        """Update the movie by id.

        Parameters
        ----------
        movie_update : MovieUpdate
            movie data to update

        movie_id : int
            movie id

        Returns
        -------
        Movie
            updated movie data
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_movie(self, movie_id: int) -> Movie:
        """Delete the movie by id.

        Parameters
        ----------
        movie_id : int
            movie id

        Returns
        -------
        Movie
            movie data
        """
        raise NotImplementedError


@final
class MovieService(SqlAlchemyServiceBase, MovieServiceBase):
    @override
    async def create_movie(self, movie_create: MovieInput, user_id: int) -> Movie:
        movie_create = MovieCreate(**movie_create.model_dump(), user_id=user_id)

        async with self.uow as uow:
            movie = await uow.movies.create(movie_create)
            await uow.commit()
            return movie

    @override
    async def get_all_movies(self, filters: MovieFilters, user_id: int) -> Sequence[Movie]:
        async with self.uow as uow:
            return await uow.movies.read_all(filters, user_id)

    @override
    async def get_movie(self, movie_id: int) -> Movie:
        """Get the movie by id.

        Parameters
        ----------
        movie_id : int
            movie id

        Returns
        -------
        Movie
            movie data

        Raises
        ------
        ResourceNotFoundError
            movie not found
        """
        async with self.uow as uow:
            movie = await uow.movies.read(movie_id)

            if movie is None:
                raise exc.ResourceNotFoundError(MSG_MOVIE_NOT_FOUND)

            return movie

    @override
    async def update_movie(self, movie_update: MovieUpdate, movie_id: int) -> Movie:
        """Update the movie by id.

        Parameters
        ----------
        movie_update : MovieUpdate
            movie data to update

        movie_id : int
            movie id

        Returns
        -------
        Movie
            updated movie data

        Raises
        ------
        ResourceNotFoundError
            movie not found
        """
        async with self.uow as uow:
            movie = await uow.movies.update(movie_id, movie_update)

            if movie is None:
                raise exc.ResourceNotFoundError(MSG_MOVIE_NOT_FOUND)

            await uow.commit()
            return movie

    @override
    async def delete_movie(self, movie_id: int) -> Movie:
        """Delete the movie by id.

        Parameters
        ----------
        movie_id : int
            movie id

        Returns
        -------
        Movie
            movie data

        Raises
        ------
        ResourceNotFoundError
            movie not found
        """
        async with self.uow as uow:
            movie = await uow.movies.delete(movie_id)

            if movie is None:
                raise exc.ResourceNotFoundError(MSG_MOVIE_NOT_FOUND)

            await uow.commit()
            return movie
