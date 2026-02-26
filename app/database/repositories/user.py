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
    select,
)

import app.core.exceptions as exc
from app.database.models import (
    UserModel,
)
from app.database.repositories.base import (
    BaseDatabaseRepository,
    BaseSqlAlchemyRepository,
)
from app.domains import (
    UserCreateDM,
    UserFiltersDM,
    UserUpdateDM,
)


class BaseUserRepository[SessionType](
    BaseDatabaseRepository[
        UserModel,
        UserCreateDM,
        UserUpdateDM,
        UserFiltersDM,
        SessionType,
    ],
):
    """Basic abstract user repository class."""

    @abstractmethod
    async def read_by_name(
        self,
        username: str,
    ) -> UserModel | None:
        """
        Read a user by username.

        Parameters
        ----------
        username : str
            user name

        Returns
        -------
        UserModel | None
            user model
        """
        raise NotImplementedError

    @override
    @abstractmethod
    async def read_all(
        self,
        filters: UserFiltersDM,
        relation_id: int | UUID | None = None,
    ) -> Sequence[UserModel]:
        """
        Read all users with the search filter.

        Parameters
        ----------
        filters : UserFiltersDM
            user search filter

        relation_id : int | UUID | None, optional
            relationship id, by default None

        Returns
        -------
        Sequence[UserModel]
            list of users
        """
        raise NotImplementedError


@final
class UserRepository(
    BaseSqlAlchemyRepository[
        UserModel,
        UserCreateDM,
        UserUpdateDM,
        UserFiltersDM,
    ],
    BaseUserRepository[AsyncSession],
):
    """SqlAlchemy user repository."""

    model_class = UserModel

    @override
    async def read_by_name(
        self,
        username: str,
    ) -> UserModel | None:
        query = select(self.model_class).where(self.model_class.username == username)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    @override
    async def read_all(
        self,
        filters: UserFiltersDM,
        relation_id: int | UUID | None = None,
    ) -> Sequence[UserModel]:
        return await super().read_all(
            filters=filters,
            relation_id=relation_id,
        )

    @classmethod
    @override
    async def _filter_query(
        cls,
        query: Select[tuple[UserModel]],
        filters: UserFiltersDM,
        relation_id: int | UUID | None,
    ) -> Select[tuple[UserModel]]:
        if (username := filters.username_contains) is not None:
            query = query.where(cls.model_class.username.ilike(f"%{username}%"))

        if (roles := filters.role) is not None:
            query = query.where(cls.model_class.role.in_(roles))

        if hasattr(cls.model_class, filters.sort_by.removeprefix("-")):
            sort_attr = getattr(cls.model_class, filters.sort_by.removeprefix("-"))
        else:
            raise exc.QueryValueError(
                query_value=filters.sort_by.removeprefix("-"),
                query_key="sort-by",
            )

        sort_by = sort_attr.desc() if filters.sort_by.startswith("-") else sort_attr.asc()

        return query.order_by(sort_by).limit(filters.limit).offset(filters.offset)
