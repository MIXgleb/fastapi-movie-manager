from abc import abstractmethod
from collections.abc import Sequence
from typing import final, override

from sqlalchemy import Select

import app.core.exceptions as exc
from app.database.models import Movie
from app.database.repositories.base import (
    BaseDatabaseRepository,
    BaseSqlAlchemyRepository,
)
from app.domains import MovieFilterDM


class BaseMovieRepository(
    BaseDatabaseRepository[
        Movie,
        MovieFilterDM,
    ],
):
    @override
    @abstractmethod
    async def read_all(
        self,
        filters: MovieFilterDM,
        relation_id: int | None,
    ) -> Sequence[Movie]:
        raise NotImplementedError


@final
class MovieRepository(
    BaseSqlAlchemyRepository[
        Movie,
        MovieFilterDM,
    ],
    BaseMovieRepository,
):
    model = Movie

    @override
    async def read_all(
        self,
        filters: MovieFilterDM,
        relation_id: int | None,
    ) -> Sequence[Movie]:
        return await super().read_all(filters, relation_id)

    @classmethod
    @override
    async def _filter_query(
        cls,
        query: Select[tuple[Movie]],
        filters: MovieFilterDM,
        relation_id: int,
    ) -> Select[tuple[Movie]]:
        query = query.where(cls.model.user_id == relation_id)

        if (title := filters.title_contains) is not None:
            query = query.where(cls.model.title.ilike(f"%{title}%"))
        if hasattr(cls.model, filters.sort_by.removeprefix("-")):
            sort_attr = getattr(cls.model, filters.sort_by.removeprefix("-"))
        else:
            raise exc.QueryValueError(filters.sort_by.removeprefix("-"), "sort-by")

        sort_by = sort_attr.desc() if filters.sort_by.startswith("-") else sort_attr.asc()

        return (
            query
            .where(cls.model.rate.between(filters.rate_from, filters.rate_to))
            .order_by(sort_by)
            .limit(filters.limit)
            .offset(filters.offset)
        )
