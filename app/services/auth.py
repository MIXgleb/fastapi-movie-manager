from abc import abstractmethod
from typing import final, override

from fastapi import Response

import app.core.exceptions as exc
from app.core.security import PasswordHelper, TokenHelper
from app.database.models import User
from app.schemas import Payload, Token, TokensCreate, UserCreate, UserInput
from app.services.base import ServiceBase, SqlAlchemyServiceBase


class AuthServiceBase(ServiceBase):
    @abstractmethod
    async def login(self, user_input: UserInput, response: Response) -> None:
        """Log in to the account.

        Parameters
        ----------
        user_input : UserInput
            user credentials

        response : Response
            response to the client
        """
        raise NotImplementedError

    @abstractmethod
    async def register(self, user_input: UserInput) -> None:
        """Register a new user.

        Parameters
        ----------
        user_input : UserInput
            user credentials
        """
        raise NotImplementedError


@final
class AuthService(SqlAlchemyServiceBase, AuthServiceBase):
    async def _check_user(self, user_input: UserInput) -> User:
        async with self.uow as uow:
            user = await uow.users.read_by_name(user_input.username)

            if user is None:
                exc_msg = "User not found."
                raise exc.AuthorizationError(exc_msg)

            if not PasswordHelper.verify(user_input.password, user.hashed_password):
                exc_msg = "Authorization failed."
                raise exc.AuthorizationError(exc_msg)

            return user

    @override
    async def login(self, user_input: UserInput, response: Response) -> None:
        user = await self._check_user(user_input)

        access_token = TokenHelper.create(
            Payload(user_id=user.id, user_role=user.role, token_type=Token.access_token)
        )
        refresh_token = TokenHelper.create(
            Payload(user_id=user.id, user_role=user.role, token_type=Token.refresh_token)
        )
        tokens = TokensCreate(access_token=access_token, refresh_token=refresh_token)
        TokenHelper.install(tokens, response)

    @override
    async def register(self, user_input: UserInput) -> None:
        """Register a new user.

        Parameters
        ----------
        user_input : UserInput
            user credentials

        Raises
        ------
        UserExistsError
            user already exists
        """
        async with self.uow as uow:
            user = await uow.users.read_by_name(user_input.username)

            if user is not None:
                raise exc.UserExistsError

            user_create = UserCreate(
                username=user_input.username,
                hashed_password=PasswordHelper.hash(user_input.password),
                role="user",
            )

            await uow.users.create(user_create)
            await uow.commit()
