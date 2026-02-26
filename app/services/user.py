from abc import (
    abstractmethod,
)
from collections.abc import (
    Sequence,
)
from datetime import (
    UTC,
    datetime,
)
from typing import (
    Any,
    Final,
    final,
    override,
)
from uuid import (
    UUID,
)

from fastapi import (
    Request,
    Response,
)

import app.core.exceptions as exc
from app.database.db_managers import (
    SqlAlchemyDatabaseManager,
)
from app.database.unit_of_works import (
    SqlAlchemyUOW,
)
from app.domains import (
    UserFiltersDM,
    UserHashedUpdateDM,
    UserOutputDM,
    UserRole,
    UserUpdateDM,
)
from app.security import (
    ZERO_IDS,
    Payload,
)
from app.security.auth_managers import (
    BaseAuthManager,
)
from app.security.password_managers import (
    BasePasswordManager,
)
from app.services.base import (
    BaseService,
    BaseSqlAlchemyService,
)

UserNotFoundError: Final[Exception] = exc.ResourceNotFoundError("User not found.")


class BaseUserService(BaseService):
    """Basic abstract user service class."""

    @abstractmethod
    async def get_all_users(
        self,
        filters: UserFiltersDM,
    ) -> Sequence[UserOutputDM]:
        """
        Get a filtered users.

        Parameters
        ----------
        filters : UserFiltersDM
            user search filter

        Returns
        -------
        Sequence[UserOutputDM]
            list of users
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user(
        self,
        user_id: UUID,
    ) -> UserOutputDM:
        """
        Get a user by id.

        Parameters
        ----------
        user_id : UUID
            user id

        Returns
        -------
        UserOutputDM
            user data

        Raises
        ------
        UserNotFoundError
            user not found
        """
        raise NotImplementedError

    @abstractmethod
    async def update_user(
        self,
        user_id: UUID,
        user_update: UserUpdateDM,
        request: Request,
        response: Response,
    ) -> None:
        """
        Update a user by id.

        Parameters
        ----------
        user_id : UUID
            user id

        user_update : UserUpdateDM
            user data to update

        request : Request
            request from the client

        response : Response
            response to the client

        Raises
        ------
        UserNotFoundError
            user not found
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_user(
        self,
        user_id: UUID,
        request: Request,
        response: Response,
    ) -> UserOutputDM:
        """
        Delete a user by id.

        Parameters
        ----------
        user_id : UUID
            user id

        request : Request
            request from the client

        response : Response
            response to the client

        Returns
        -------
        UserOutputDM
            user data

        Raises
        ------
        UserNotFoundError
            user not found
        """
        raise NotImplementedError


@final
class UserService(
    BaseSqlAlchemyService,
    BaseUserService,
):
    """SqlAlchemy user service."""

    __slots__ = ("auth_manager", "password_manager")

    @override
    def __init__(
        self,
        uow_class: type[SqlAlchemyUOW],
        database_manager: SqlAlchemyDatabaseManager,
        password_manager: BasePasswordManager,
        auth_manager: BaseAuthManager[Any, Any, Any, Any, Any],
    ) -> None:
        """
        Initialize the user service.

        Parameters
        ----------
        uow_class : type[SqlAlchemyUOW]
            sqlalchemy database unit-of-work class

        database_manager : SqlAlchemyDatabaseManager
            sqlalchemy database manager

        password_manager : BasePasswordManager
            password manager

        auth_manager : BaseAuthManager
            token manager
        """
        super().__init__(
            uow_class=uow_class,
            database_manager=database_manager,
        )
        self.password_manager = password_manager
        self.auth_manager = auth_manager

    @override
    async def get_all_users(
        self,
        filters: UserFiltersDM,
    ) -> Sequence[UserOutputDM]:
        async with self.uow as uow:
            users = await uow.users.read_all(filters)
            return [UserOutputDM.from_object(user) for user in users]

    @override
    async def get_user(
        self,
        user_id: UUID,
    ) -> UserOutputDM:
        if user_id in ZERO_IDS:
            return UserOutputDM(
                username=UserRole.GUEST,
                role=UserRole.GUEST,
                created_at=datetime.now(UTC),
            )

        async with self.uow as uow:
            user = await uow.users.read(user_id)

            if user is None:
                raise UserNotFoundError

            return UserOutputDM.from_object(user)

    @override
    async def update_user(
        self,
        user_id: UUID,
        user_update: UserUpdateDM,
        request: Request,
        response: Response,
    ) -> None:
        user_hashed_update = UserHashedUpdateDM.from_object(
            user_update,
            none_if_key_not_found=True,
            hashed_password=self.password_manager.hash(user_update.password)
            if user_update.password is not None
            else None,
        )

        async with self.uow as uow:
            user = await uow.users.update(
                item_id=user_id,
                item_update=user_hashed_update,
            )

            if user is None:
                raise UserNotFoundError

            await self.auth_manager.update_tokens(
                updated_payload=Payload(
                    user_id=user.id,
                    user_role=user.role,
                ),
                request=request,
                response=response,
            )

    @override
    async def delete_user(
        self,
        user_id: UUID,
        request: Request,
        response: Response,
    ) -> UserOutputDM:
        async with self.uow as uow:
            user = await uow.users.delete(user_id)

            if user is None:
                raise UserNotFoundError

            await self.auth_manager.clear_tokens(
                request=request,
                response=response,
                user_id=user_id,
            )
            return UserOutputDM.from_object(user)
