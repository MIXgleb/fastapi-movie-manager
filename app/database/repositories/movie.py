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
from uuid import (
    UUID,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.sql.expression import (
    Select,
)

import app.core.exceptions as exc
from app.database.models import (
    MovieModel,
)
from app.database.repositories.base import (
    BaseDatabaseRepository,
    BaseSqlAlchemyRepository,
)
from app.domains import (
    MovieCreateDM,
    MovieFiltersDM,
    MovieUpdateDM,
)


class BaseMovieRepository[SessionType](
    BaseDatabaseRepository[
        MovieModel,
        MovieCreateDM,
        MovieUpdateDM,
        MovieFiltersDM,
        SessionType,
    ],
):
    """Basic abstract movie repository class."""

    @override
    @abstractmethod
    async def read_all(
        self,
        filters: MovieFiltersDM,
        relation_id: int | UUID | None,
    ) -> Sequence[MovieModel]:
        """
        Read all movies with the search filter.

        Parameters
        ----------
        filters : MovieFiltersDM
            movie search filter

        relation_id : int | UUID | None
            relationship id

        Returns
        -------
        Sequence[MovieModel]
            list of movies

        Raises
        ------
        TypeError
            missing 'relation_id' argument
        """
        raise NotImplementedError


@final
class MovieRepository(
    BaseSqlAlchemyRepository[
        MovieModel,
        MovieCreateDM,
        MovieUpdateDM,
        MovieFiltersDM,
    ],
    BaseMovieRepository[AsyncSession],
):
    """SqlAlchemy movie repository."""

    model_class = MovieModel

    @override
    async def read_all(
        self,
        filters: MovieFiltersDM,
        relation_id: int | UUID | None,
    ) -> Sequence[MovieModel]:
        if relation_id is None:
            exc_msg = (
                f"{self.model_class}.read_all() missing 1 required "
                "positional argument: 'relation_id'"
            )
            raise TypeError(exc_msg)

        return await super().read_all(
            filters=filters,
            relation_id=relation_id,
        )

    @classmethod
    @override
    async def _filter_query(
        cls,
        query: Select[tuple[MovieModel]],
        filters: MovieFiltersDM,
        relation_id: int | UUID | None,
    ) -> Select[tuple[MovieModel]]:
        query = query.where(cls.model_class.user_id == relation_id)

        if (title := filters.title_contains) is not None:
            query = query.where(cls.model_class.title.ilike(f"%{title}%"))

        if hasattr(cls.model_class, filters.sort_by.removeprefix("-")):
            sort_attr = getattr(cls.model_class, filters.sort_by.removeprefix("-"))
        else:
            raise exc.QueryValueError(
                query_value=filters.sort_by.removeprefix("-"),
                query_key="sort-by",
            )

        sort_by = sort_attr.desc() if filters.sort_by.startswith("-") else sort_attr.asc()

        return (
            query.where(
                cls.model_class.rate.between(
                    cleft=filters.rate_from,
                    cright=filters.rate_to,
                ),
            )
            .order_by(sort_by)
            .limit(filters.limit)
            .offset(filters.offset)
        )
