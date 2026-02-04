from abc import abstractmethod
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import final, override

from fastapi import Request, Response

import app.core.exceptions as exc
from app.api.v1.schemas import (
    UserFilterDTO,
    UserOutputDTO,
    UserUpdateDTO,
    UserUpdateWithHashedPasswordDTO,
)
from app.core.constants import MESSAGE_USER_NOT_FOUND
from app.domains import UserFilterDM, UserRole
from app.security import (
    Payload,
    password_helper,
    token_helper,
)
from app.services.base import BaseService, BaseSqlAlchemyService


class BaseUserService(BaseService):
    @abstractmethod
    async def get_all_users(
        self,
        filters: UserFilterDTO,
    ) -> Sequence[UserOutputDTO]:
        """Get the filtered users.

        Parameters
        ----------
        filters : UserFilterDTO
            user search filter

        Returns
        -------
        Sequence[UserOutputDTO]
            list of users
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user(
        self,
        user_id: int,
    ) -> UserOutputDTO:
        """Get the user by id.

        Parameters
        ----------
        user_id : int
            user id

        Returns
        -------
        UserOutputDTO
            user data

        Raises
        ------
        ResourceNotFoundError
            user not found
        """
        raise NotImplementedError

    @abstractmethod
    async def update_user(
        self,
        user_id: int,
        user_update: UserUpdateDTO,
        request: Request,
        response: Response,
    ) -> None:
        """Update the user by id.

        Parameters
        ----------
        user_id : int
            user id

        user_update : UserUpdateDTO
            user data to update

        request : Request
            request from the client

        response : Response
            response to the client

        Raises
        ------
        ResourceNotFoundError
            user not found
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_user(
        self,
        user_id: int,
        request: Request,
        response: Response,
    ) -> UserOutputDTO:
        """Delete the user by id.

        Parameters
        ----------
        user_id : int
            user id

        request : Request
            request from the client

        response : Response
            response to the client

        Returns
        -------
        UserOutputDTO
            user data

        Raises
        ------
        ResourceNotFoundError
            user not found
        """
        raise NotImplementedError


@final
class UserService(BaseSqlAlchemyService, BaseUserService):
    @override
    async def get_all_users(
        self,
        filters: UserFilterDTO,
    ) -> Sequence[UserOutputDTO]:
        async with self.uow as uow:
            users = await uow.users.read_all(
                filters=UserFilterDM(
                    **filters.model_dump(),
                ),
            )
            return [UserOutputDTO.model_validate(user) for user in users]

    @override
    async def get_user(
        self,
        user_id: int,
    ) -> UserOutputDTO:
        if user_id == 0:
            return UserOutputDTO(
                username="guest",
                id=0,
                role=UserRole.guest,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )

        async with self.uow as uow:
            user = await uow.users.read(user_id)

            if user is None:
                raise exc.ResourceNotFoundError(MESSAGE_USER_NOT_FOUND)

            return UserOutputDTO.model_validate(user)

    @override
    async def update_user(
        self,
        user_id: int,
        user_update: UserUpdateDTO,
        request: Request,
        response: Response,
    ) -> None:
        async with self.uow as uow:
            user_update_hashed_pwd = UserUpdateWithHashedPasswordDTO(
                **user_update.model_dump(exclude_unset=True),
                hashed_password=password_helper.hash(user_update.password),
            )
            user = await uow.users.update(
                item_id=user_id,
                item_update=user_update_hashed_pwd.model_dump(exclude_unset=True),
            )

            if user is None:
                raise exc.ResourceNotFoundError(MESSAGE_USER_NOT_FOUND)

            payload = Payload(
                user_id=user.id,
                user_role=user.role,
            )
            await token_helper.update_tokens(
                updated_payload=payload,
                request=request,
                response=response,
            )

    @override
    async def delete_user(
        self,
        user_id: int,
        request: Request,
        response: Response,
    ) -> UserOutputDTO:
        async with self.uow as uow:
            user = await uow.users.delete(user_id)

            if user is None:
                raise exc.ResourceNotFoundError(MESSAGE_USER_NOT_FOUND)

            await token_helper.clear_tokens(
                request=request,
                response=response,
                user_id=user_id,
            )
            return UserOutputDTO.model_validate(user)
