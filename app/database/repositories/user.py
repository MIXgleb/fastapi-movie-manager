from abc import abstractmethod
from collections.abc import Sequence
from typing import final, override

from sqlalchemy import Select, select

import app.core.exceptions as exc
from app.database.models import User
from app.database.repositories.base import (
    BaseDatabaseRepository,
    BaseSqlAlchemyRepository,
)
from app.domains import UserFilterDM


class BaseUserRepository(
    BaseDatabaseRepository[User, UserFilterDM],
):
    @abstractmethod
    async def read_by_name(self, username: str) -> User | None:
        """Read the user by username.

        Parameters
        ----------
        username : str
            user name

        Returns
        -------
        User | None
            user model
        """
        raise NotImplementedError

    @override
    @abstractmethod
    async def read_all(
        self,
        filters: UserFilterDM,
        _relation_id: int | None = None,
    ) -> Sequence[User]:
        """Read all users with the search filter.

        Parameters
        ----------
        filters : UserFilterDM
            user search filter

        Returns
        -------
        Sequence[User]
            list of users
        """
        raise NotImplementedError


@final
class UserRepository(
    BaseSqlAlchemyRepository[User, UserFilterDM],
    BaseUserRepository,
):
    model = User

    @override
    async def read_by_name(self, username: str) -> User | None:
        query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    @override
    async def read_all(
        self,
        filters: UserFilterDM,
        _relation_id: int | None = None,
    ) -> Sequence[User]:
        return await super().read_all(filters, -1)

    @classmethod
    @override
    async def _filter_query(
        cls,
        query: Select[tuple[User]],
        filters: UserFilterDM,
        _relation_id: int,
    ) -> Select[tuple[User]]:
        if (username := filters.username_contains) is not None:
            query = query.where(cls.model.username.ilike(f"%{username}%"))
        if (roles := filters.role) is not None:
            query = query.where(cls.model.role.in_(roles))
        if hasattr(cls.model, filters.sort_by.removeprefix("-")):
            sort_attr = getattr(cls.model, filters.sort_by.removeprefix("-"))
        else:
            raise exc.QueryValueError(filters.sort_by.removeprefix("-"), "sort-by")

        sort_by = sort_attr.desc() if filters.sort_by.startswith("-") else sort_attr.asc()
        return query.order_by(sort_by).limit(filters.limit).offset(filters.offset)
