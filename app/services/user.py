from abc import abstractmethod
from collections.abc import Sequence
from typing import Final, final, override

import app.core.exceptions as exc
from app.database.models import User
from app.schemas import UserFilters
from app.services.base import ServiceBase, SqlAlchemyServiceBase

MSG_USER_NOT_FOUND: Final[str] = "User not found."


class UserServiceBase(ServiceBase):
    @abstractmethod
    async def get_all_users(self, filters: UserFilters) -> Sequence[User]:
        """Get the filtered users.

        Parameters
        ----------
        filters : UserFilters
            user search filter

        Returns
        -------
        Sequence[User]
            list of users
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: int) -> User:
        """Get the user by id.

        Parameters
        ----------
        user_id : int
            user id

        Returns
        -------
        User
            user data
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: int) -> User:
        """Delete the user by id.

        Parameters
        ----------
        user_id : int
            user id

        Returns
        -------
        User
            user data
        """
        raise NotImplementedError


@final
class UserService(SqlAlchemyServiceBase, UserServiceBase):
    @override
    async def get_all_users(self, filters: UserFilters) -> Sequence[User]:
        async with self.uow as uow:
            return await uow.users.read_all(filters)

    @override
    async def get_user(self, user_id: int) -> User:
        """Get the user by id.

        Parameters
        ----------
        user_id : int
            user id

        Returns
        -------
        User
            user data

        Raises
        ------
        ResourceNotFoundError
            user not found
        """
        async with self.uow as uow:
            user = await uow.users.read(user_id)

            if user is None:
                raise exc.ResourceNotFoundError(MSG_USER_NOT_FOUND)

            return user

    @override
    async def delete_user(self, user_id: int) -> User:
        """Delete the user by id.

        Parameters
        ----------
        user_id : int
            user id

        Returns
        -------
        User
            user data

        Raises
        ------
        ResourceNotFoundError
            user not found
        """
        async with self.uow as uow:
            user = await uow.users.delete(user_id)

            if user is None:
                raise exc.ResourceNotFoundError(MSG_USER_NOT_FOUND)

            await uow.commit()
            return user
