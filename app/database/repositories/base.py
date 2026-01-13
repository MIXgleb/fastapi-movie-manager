from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, final, override

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.domains import DataclassType

type TypeDictAnyAny = dict[Any, Any]


class BaseDatabaseRepository[
    Model,
    Filter,
](ABC):
    @abstractmethod
    async def create(
        self,
        item_create: TypeDictAnyAny,
    ) -> Model:
        """Create a new item.

        Parameters
        ----------
        item_create : DictAny
            item data to create

        Returns
        -------
        Model
            created item model
        """
        raise NotImplementedError

    @abstractmethod
    async def read(
        self,
        item_id: int,
    ) -> Model | None:
        """Read the item by id.

        Parameters
        ----------
        item_id : int
            item id

        Returns
        -------
        Model | None
            item model
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        item_id: int,
        item_update: TypeDictAnyAny,
    ) -> Model | None:
        """Update the item by id.

        Parameters
        ----------
        item_id : int
            item id

        item_update : DictAny
            item data to update

        Returns
        -------
        Model | None
            updated item model
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        item_id: int,
    ) -> Model | None:
        """Delete the item by id.

        Parameters
        ----------
        item_id : int
            item id

        Returns
        -------
        Model | None
            item model
        """
        raise NotImplementedError

    @abstractmethod
    async def read_all(
        self,
        filters: Filter,
        _relation_id: int | None,
    ) -> Sequence[Model]:
        """Read all items with the search filter.

        Parameters
        ----------
        filters : Filter
            item search filter

        relation_id : int | None
            relationship id

        Returns
        -------
        Sequence[Model]
            list of items

        Raises
        ------
        TypeError
            missing 'relation_id' argument
        """
        raise NotImplementedError


class BaseSqlAlchemyRepository[
    Model: DeclarativeBase,
    Filter: DataclassType,
](
    BaseDatabaseRepository[
        Model,
        Filter,
    ],
):
    __slots__ = ("session",)

    model: type[Model]

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Initialize the sqlalchemy repository.

        Parameters
        ----------
        session : AsyncSession
            instance of the database connection session
        """
        self.session = session

    @final
    @override
    async def create(
        self,
        item_create: TypeDictAnyAny,
    ) -> Model:
        new_item = self.model(**item_create)
        self.session.add(new_item)
        await self.session.flush()
        return new_item

    @final
    @override
    async def read(
        self,
        item_id: int,
    ) -> Model | None:
        return await self.session.get(self.model, item_id)

    @final
    @override
    async def update(
        self,
        item_id: int,
        item_update: TypeDictAnyAny,
    ) -> Model | None:
        item = await self.read(item_id)

        if item is None:
            return None

        for key, value in item_update.items():
            setattr(item, key, value)

        await self.session.flush()
        return item

    @final
    @override
    async def delete(
        self,
        item_id: int,
    ) -> Model | None:
        item = await self.read(item_id)

        if item is None:
            return None

        await self.session.delete(item)
        return item

    @override
    async def read_all(
        self,
        filters: Filter,
        _relation_id: int | None,
    ) -> Sequence[Model]:
        if _relation_id is None:
            msg_err = (
                f"{self.model}.read_all() missing 1 required "
                "positional argument: 'relation_id'"
            )
            raise TypeError(msg_err)

        query = select(self.model)
        query = await self._filter_query(query, filters, _relation_id)
        result = await self.session.scalars(query)
        return result.all()

    @classmethod
    async def _filter_query(
        cls,
        query: Select[tuple[Model]],
        _filters: Filter,
        _relation_id: int,
    ) -> Select[tuple[Model]]:
        """Filter the query by the specified search filter.

        Parameters
        ----------
        query : Select[tuple[Model]]
            database query expression

        _filters : Filter
            item search filter

        _relation_id : int
            relationship id

        Returns
        -------
        Select[tuple[Model]]
            filtered query expression
        """
        return query
