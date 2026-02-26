from abc import (
    ABC,
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
    select,
)

from app.database.models import (
    BaseModel,
)
from app.domains import (
    BaseDataclass,
)


class BaseDatabaseRepository[
    ModelType,
    ItemCreateType,
    ItemUpdateType,
    FiltersType,
    SessionType,
](ABC):
    """Basic abstract database repository class."""

    __slots__ = ("session",)

    def __init__(
        self,
        session: SessionType,
    ) -> None:
        """
        Initialize the database repository.

        Parameters
        ----------
        session : SessionType
            instance of a database connection session
        """
        self.session = session

    @abstractmethod
    async def create(
        self,
        item_create: ItemCreateType,
    ) -> ModelType:
        """
        Create a new item.

        Parameters
        ----------
        item_create : ItemCreateType
            item data to create

        Returns
        -------
        ModelType
            created item model
        """
        raise NotImplementedError

    @abstractmethod
    async def read(
        self,
        item_id: int | UUID,
    ) -> ModelType | None:
        """
        Read a item by id.

        Parameters
        ----------
        item_id : int | UUID
            item id

        Returns
        -------
        ModelType | None
            item model
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        item_id: int | UUID,
        item_update: ItemUpdateType,
    ) -> ModelType | None:
        """
        Update a item by id.

        Parameters
        ----------
        item_id : int | UUID
            item id

        item_update : ItemUpdateType
            item data to update

        Returns
        -------
        ModelType | None
            updated item model
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        item_id: int | UUID,
    ) -> ModelType | None:
        """
        Delete a item by id.

        Parameters
        ----------
        item_id : int | UUID
            item id

        Returns
        -------
        ModelType | None
            item model
        """
        raise NotImplementedError

    @abstractmethod
    async def read_all(
        self,
        filters: FiltersType,
        relation_id: int | UUID | None,
    ) -> Sequence[ModelType]:
        """
        Read all items with a search filter.

        Parameters
        ----------
        filters : FiltersType
            item search filter

        relation_id : int | UUID | None
            relationship id

        Returns
        -------
        Sequence[ModelType]
            list of items
        """
        raise NotImplementedError


class BaseSqlAlchemyRepository[
    ModelType: BaseModel,
    ItemCreateType: BaseDataclass,
    ItemUpdateType: BaseDataclass,
    FiltersType: BaseDataclass,
](
    BaseDatabaseRepository[
        ModelType,
        ItemCreateType,
        ItemUpdateType,
        FiltersType,
        AsyncSession,
    ],
):
    """Basic abstract SqlAlchemy database repository class."""

    model_class: type[ModelType]

    @final
    @override
    async def create(
        self,
        item_create: ItemCreateType,
    ) -> ModelType:
        new_item = self.model_class(**item_create.as_dict())
        self.session.add(new_item)
        await self.session.flush()
        return new_item

    @final
    @override
    async def read(
        self,
        item_id: int | UUID,
    ) -> ModelType | None:
        return await self.session.get(self.model_class, item_id)

    @final
    @override
    async def update(
        self,
        item_id: int | UUID,
        item_update: ItemUpdateType,
    ) -> ModelType | None:
        item = await self.read(item_id)

        if item is None:
            return None

        for key, value in item_update.as_dict(exclude_none=True).items():
            setattr(item, key, value)

        await self.session.flush()
        return item

    @final
    @override
    async def delete(
        self,
        item_id: int | UUID,
    ) -> ModelType | None:
        item = await self.read(item_id)

        if item is None:
            return None

        await self.session.delete(item)
        return item

    @override
    async def read_all(
        self,
        filters: FiltersType,
        relation_id: int | UUID | None,
    ) -> Sequence[ModelType]:
        query = select(self.model_class)
        query = await self._filter_query(
            query=query,
            filters=filters,
            relation_id=relation_id,
        )
        result = await self.session.scalars(query)
        return result.all()

    @classmethod
    async def _filter_query(
        cls,
        query: Select[tuple[ModelType]],
        filters: FiltersType,
        relation_id: int | UUID | None,
    ) -> Select[tuple[ModelType]]:
        """
        Filter a query by the specified search filter.

        Parameters
        ----------
        query : Select[tuple[ModelType]]
            database query expression

        filters : FiltersType
            item search filter

        relation_id : int | UUID | None
            relationship id

        Returns
        -------
        Select[tuple[ModelType]]
            filtered query expression
        """
        _ = filters
        _ = relation_id
        return query
