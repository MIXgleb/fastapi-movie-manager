from abc import (
    abstractmethod,
)
from typing import (
    Any,
    final,
    override,
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
    UserCreateDM,
    UserInputDM,
    UserRole,
)
from app.security import (
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


class BaseAuthService(BaseService):
    """Basic abstract auth service class."""

    @abstractmethod
    async def login(
        self,
        user_input: UserInputDM,
        request: Request,
    ) -> None:
        """
        Log in to the account.

        Parameters
        ----------
        user_input : UserInputDM
            user credentials

        request : Request
            request from the client

        Raises
        ------
        AuthorizationError
            user not found

        AuthorizationError
            incorrect password
        """
        raise NotImplementedError

    @abstractmethod
    async def register(
        self,
        user_input: UserInputDM,
    ) -> None:
        """
        Register a new user.

        Parameters
        ----------
        user_input : UserInputDM
            user data

        Raises
        ------
        UserExistsError
            user already exists
        """
        raise NotImplementedError

    @abstractmethod
    async def logout(
        self,
        request: Request,
        response: Response,
    ) -> None:
        """
        Log out of the account.

        Parameters
        ----------
        request : Request
            request from the client

        response : Response
            response to the client
        """
        raise NotImplementedError


@final
class AuthService(
    BaseSqlAlchemyService,
    BaseAuthService,
):
    """SqlAlchemy auth service."""

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
        Initialize the auth service.

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
    async def login(
        self,
        user_input: UserInputDM,
        request: Request,
    ) -> None:
        async with self.uow as uow:
            user = await uow.users.read_by_name(user_input.username)

            if user is None:
                exc_msg = "User not found."
                raise exc.AuthorizationError(exc_msg)

            if not self.password_manager.verify(user_input.password, user.hashed_password):
                exc_msg = "Authorization failed."
                raise exc.AuthorizationError(exc_msg)

            payload = Payload(
                user_id=user.id,
                user_role=user.role,
            )
            await self.auth_manager.generate_tokens(
                payload=payload,
                request=request,
            )

    @override
    async def register(
        self,
        user_input: UserInputDM,
    ) -> None:
        user_create = UserCreateDM(
            username=user_input.username,
            hashed_password=self.password_manager.hash(user_input.password),
            role=UserRole.USER,
        )

        async with self.uow as uow:
            user = await uow.users.read_by_name(user_create.username)

            if user is not None:
                raise exc.UserExistsError

            await uow.users.create(user_create)

    @override
    async def logout(
        self,
        request: Request,
        response: Response,
    ) -> None:
        await self.auth_manager.clear_tokens(
            request=request,
            response=response,
        )
