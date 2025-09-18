from collections.abc import Sequence
from typing import final, override

from sqlalchemy import Select, select

from app.core.exceptions import QueryValueError
from app.database.models import Movie
from app.database.repositories.base import RepositoryBase, SqlAlchemyRepositoryBase
from app.schemas import MovieCreate, MovieFilters, MovieUpdate


class MovieRepositoryBase(RepositoryBase[Movie, MovieCreate, MovieUpdate, MovieFilters]):
    @override
    async def read_all(self, filters: MovieFilters, relation_id: int = -1) -> Sequence[Movie]:
        """Read all movies with the search filter.

        Parameters
        ----------
        filters : MovieFilters
            movie search filter

        relation_id : int, optional
            relationship user id, by default -1

        Returns
        -------
        Sequence[Movie]
            list of movies

        Raises
        ------
        TypeError
            missing 'relation_id' argument
        """
        raise NotImplementedError


@final
class MovieRepository(
    SqlAlchemyRepositoryBase[Movie, MovieCreate, MovieUpdate, MovieFilters],
    MovieRepositoryBase,
):
    model = Movie

    @override
    async def read_all(self, filters: MovieFilters, relation_id: int = -1) -> Sequence[Movie]:
        if relation_id == -1:
            msg_err = "read_all() missing 1 required positional argument: 'relation_id'"
            raise TypeError(msg_err)

        query = select(self.model)
        query = await self._filter_query(query, filters, relation_id)
        result = await self.session.scalars(query)
        return result.all()

    @classmethod
    @override
    async def _filter_query(
        cls,
        query: Select[tuple[Movie]],
        filters: MovieFilters,
        relation_id: int = -1,
    ) -> Select[tuple[Movie]]:
        query = query.where(cls.model.user_id == relation_id)

        if (title := filters.title_contains) is not None:
            query = query.where(cls.model.title.ilike(f"%{title}%"))
        if hasattr(cls.model, filters.sort_by.removeprefix("-")):
            sort_attr = getattr(cls.model, filters.sort_by.removeprefix("-"))
        else:
            raise QueryValueError(filters.sort_by.removeprefix("-"), "sort-by")

        sort_by = sort_attr.desc() if filters.sort_by.startswith("-") else sort_attr.asc()
        return (
            query.where(filters.rate_from <= cls.model.rate <= filters.rate_to)
            .order_by(sort_by)
            .limit(filters.limit)
            .offset(filters.offset)
        )
