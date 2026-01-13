from abc import abstractmethod
from typing import final, override

from fastapi import Request, Response

import app.core.exceptions as exc
from app.api.v1.schemas import UserCreateDTO, UserInputDTO
from app.domains import UserRole
from app.security import (
    PasswordHelper,
    Payload,
    TokenHelper,
)
from app.services.base import BaseService, BaseSqlAlchemyService


class BaseAuthService(BaseService):
    @abstractmethod
    async def login(
        self,
        user_input: UserInputDTO,
        request: Request,
    ) -> None:
        """Log in to the account.

        Parameters
        ----------
        user_input : UserInputDTO
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
        user_input: UserInputDTO,
    ) -> None:
        """Register a new user.

        Parameters
        ----------
        user_input : UserInputDTO
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
        """Log out of the account.

        Parameters
        ----------
        request : Request
            request from the client

        response : Response
            response to the client
        """
        raise NotImplementedError


@final
class AuthService(BaseSqlAlchemyService, BaseAuthService):
    @override
    async def login(
        self,
        user_input: UserInputDTO,
        request: Request,
    ) -> None:
        async with self.uow as uow:
            user = await uow.users.read_by_name(user_input.username)

            if user is None:
                exc_msg = "User not found."
                raise exc.AuthorizationError(exc_msg)

            if not PasswordHelper.verify(user_input.password, user.hashed_password):
                exc_msg = "Authorization failed."
                raise exc.AuthorizationError(exc_msg)

            payload = Payload(
                user_id=user.id,
                user_role=user.role,
            )
            await TokenHelper.generate_tokens(
                payload=payload,
                request=request,
            )

    @override
    async def register(
        self,
        user_input: UserInputDTO,
    ) -> None:
        user_create = UserCreateDTO(
            username=user_input.username,
            hashed_password=PasswordHelper.hash(user_input.password),
            role=UserRole.user,
        )

        async with self.uow as uow:
            user = await uow.users.read_by_name(user_create.username)

            if user is not None:
                raise exc.UserExistsError

            await uow.users.create(user_create.model_dump())

    @override
    async def logout(
        self,
        request: Request,
        response: Response,
    ) -> None:
        await TokenHelper.clear_tokens(
            request=request,
            response=response,
        )
