from abc import abstractmethod
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Final, final, override

from fastapi import Response

import app.core.exceptions as exc
from app.api.v1.schemas import (
    UserFilterDTO,
    UserOutputDTO,
    UserUpdateDTO,
    UserUpdateWithHashedPasswordDTO,
)
from app.core.security import (
    JWTokenReadDTO,
    PasswordHelper,
    Payload,
    TokenHelper,
)
from app.domains import UserFilterDM, UserRole
from app.services.base import ServiceBase, SqlAlchemyServiceBase

MSG_USER_NOT_FOUND: Final[str] = "User not found."


class UserServiceBase(ServiceBase):
    @abstractmethod
    async def get_all_users(self, filters: UserFilterDTO) -> Sequence[UserOutputDTO]:
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
    async def get_user(self, user_id: int) -> UserOutputDTO:
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
        tokens: JWTokenReadDTO,
        response: Response,
    ) -> None:
        """Update the user by id.

        Parameters
        ----------
        user_id : int
            user id

        user_update : UserUpdateDTO
            user data to update

        tokens : JWTokenReadDTO
            client's tokens

        response : Response
            response from the endpoint

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
        tokens: JWTokenReadDTO,
        response: Response,
    ) -> UserOutputDTO:
        """Delete the user by id.

        Parameters
        ----------
        user_id : int
            user id

        tokens : JWTokenReadDTO
            client's tokens

        response : Response
            response from the endpoint

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
class UserService(SqlAlchemyServiceBase, UserServiceBase):
    @override
    async def get_all_users(self, filters: UserFilterDTO) -> Sequence[UserOutputDTO]:
        async with self.uow as uow:
            filter_dm = UserFilterDM(
                limit=filters.limit,
                offset=filters.offset,
                sort_by=filters.sort_by,
                username_contains=filters.username_contains,
                role=filters.role,
            )
            users = await uow.users.read_all(filter_dm)
            return [UserOutputDTO.model_validate(user) for user in users]

    @override
    async def get_user(self, user_id: int) -> UserOutputDTO:
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
                raise exc.ResourceNotFoundError(MSG_USER_NOT_FOUND)

            return UserOutputDTO.model_validate(user)

    @override
    async def update_user(
        self,
        user_id: int,
        user_update: UserUpdateDTO,
        tokens: JWTokenReadDTO,
        response: Response,
    ) -> None:
        async with self.uow as uow:
            user_update_hashed_pwd = UserUpdateWithHashedPasswordDTO(
                **user_update.model_dump(exclude_unset=True),
                hashed_password=PasswordHelper.hash(user_update.password),
            )
            user = await uow.users.update(
                item_id=user_id,
                item_update=user_update_hashed_pwd.model_dump(exclude_unset=True),
            )

            if user is None:
                raise exc.ResourceNotFoundError(MSG_USER_NOT_FOUND)

            payload = Payload(
                user_id=user.id,
                user_role=user.role,
            )
            await TokenHelper.update_tokens(tokens, response, payload)

    @override
    async def delete_user(
        self,
        user_id: int,
        tokens: JWTokenReadDTO,
        response: Response,
    ) -> UserOutputDTO:
        async with self.uow as uow:
            user = await uow.users.delete(user_id)

            if user is None:
                raise exc.ResourceNotFoundError(MSG_USER_NOT_FOUND)

            await TokenHelper.clear_tokens(tokens, response, user_id)
            return UserOutputDTO.model_validate(user)
