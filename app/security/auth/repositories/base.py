import asyncio
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    final,
    override,
)

from fastapi import (
    Response,
)
from pydantic import (
    BaseModel as BaseSchema,
)

from app.security.auth.schemas import (
    BaseAuthTokenDTO,
    BasePayload,
)
from app.security.auth.tokens import (
    BaseAsyncAuthToken,
    BaseAuthToken,
    BaseSyncAuthToken,
)

type SyncOrAsyncAuthTokenType[
    TokenType,
    TokenKeyType,
    PayloadType: BasePayload,
    TokenConfigType: BaseSchema,
] = (
    BaseSyncAuthToken[TokenType, TokenKeyType, PayloadType, TokenConfigType]
    | BaseAsyncAuthToken[TokenType, TokenKeyType, PayloadType, TokenConfigType]
)


class BaseAuthTokenRepository[
    TokenKeyType,
    PayloadType: BasePayload,
    TokenType: BaseAuthToken[Any, Any],
](ABC):
    """Basic abstract auth token repository class."""

    @classmethod
    @abstractmethod
    async def create_tokens(
        cls,
        access_token: TokenType,
        refresh_token: TokenType,
        payload: PayloadType,
    ) -> BaseAuthTokenDTO:
        """
        Create all tokens.

        Parameters
        ----------
        access_token : TokenType
            access token instance

        refresh_token : TokenType
            refresh token instance

        payload : PayloadType
            payload data

        Returns
        -------
        BaseTokenDTO
            created tokens
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def read_token(
        cls,
        token: TokenType,
    ) -> PayloadType:
        """
        Read all tokens.

        Parameters
        ----------
        token : TokenType
            token instance

        Returns
        -------
        PayloadType
            payload data
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def update_tokens(
        cls,
        access_token: TokenType,
        refresh_token: TokenType,
        response: Response,
        payload: PayloadType,
    ) -> None:
        """
        Update all tokens.

        Parameters
        ----------
        access_token : TokenType
            access token instance

        refresh_token : TokenType
            refresh token instance

        response : Response
            response to the client

        payload : PayloadType
            payload data
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def delete_tokens(
        cls,
        access_token: TokenType,
        refresh_token: TokenType,
        response: Response,
        key: TokenKeyType | None = None,
    ) -> None:
        """
        Delete tokens.

        Parameters
        ----------
        access_token : TokenType
            access token instance

        refresh_token : TokenType
            refresh token instance

        response : Response
            response to the client

        key : TokenKeyType | None, optional
            unique key, by default None
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def save_tokens(
        cls,
        access_token: TokenType,
        refresh_token: TokenType,
        response: Response,
        payload: PayloadType | None,
    ) -> None:
        """
        Save tokens.

        Parameters
        ----------
        access_token : TokenType
            access token instance

        refresh_token : TokenType
            refresh token instance

        response : Response
            response to the client

        payload : PayloadType | None
            payload data
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def is_user_initiator(
        cls,
        payload_initiator: PayloadType,
        key: TokenKeyType,
    ) -> bool:
        """
        Check if a user is initiator.

        Parameters
        ----------
        payload_initiator : PayloadType
            payload data

        key : TokenKeyType
            unique key

        Returns
        -------
        bool
            verification status
        """
        raise NotImplementedError


class BaseSyncAsyncAuthTokenRepository[
    TokenKeyType,
    PayloadType: BasePayload,
    TokenConfigType: BaseSchema,
](
    BaseAuthTokenRepository[
        TokenKeyType,
        PayloadType,
        SyncOrAsyncAuthTokenType[
            Any,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
    ],
):
    """Basic abstract sync and async auth token repository class."""

    @final
    @classmethod
    @override
    async def create_tokens[TokenType](
        cls,
        access_token: SyncOrAsyncAuthTokenType[
            TokenType,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
        refresh_token: SyncOrAsyncAuthTokenType[
            TokenType,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
        payload: PayloadType,
    ) -> BaseAuthTokenDTO:
        access_token_create_result = access_token.create(payload)
        refresh_token_create_result = refresh_token.create(payload)

        if asyncio.iscoroutine(access_token_create_result):
            access_token_value = await access_token_create_result
        else:
            access_token_value = access_token_create_result
        if asyncio.iscoroutine(refresh_token_create_result):
            refresh_token_value = await refresh_token_create_result
        else:
            refresh_token_value = refresh_token_create_result

        return BaseAuthTokenDTO(
            access_token=access_token_value,
            refresh_token=refresh_token_value,
        )

    @final
    @classmethod
    @override
    async def read_token[TokenType](
        cls,
        token: SyncOrAsyncAuthTokenType[
            TokenType,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
    ) -> PayloadType:
        payload: PayloadType
        token_read_result = token.read()

        if asyncio.iscoroutine(token_read_result):
            payload = await token_read_result
        else:
            payload = token_read_result

        return payload

    @final
    @classmethod
    @override
    async def update_tokens[TokenType](
        cls,
        access_token: SyncOrAsyncAuthTokenType[
            TokenType,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
        refresh_token: SyncOrAsyncAuthTokenType[
            TokenType,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
        response: Response,
        payload: PayloadType,
    ) -> None:
        access_token_update_result = access_token.update(response, payload)
        refresh_token_update_result = refresh_token.update(response, payload)

        if asyncio.iscoroutine(access_token_update_result):
            await access_token_update_result
        if asyncio.iscoroutine(refresh_token_update_result):
            await refresh_token_update_result

    @final
    @classmethod
    @override
    async def delete_tokens[TokenType](
        cls,
        access_token: SyncOrAsyncAuthTokenType[
            TokenType,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
        refresh_token: SyncOrAsyncAuthTokenType[
            TokenType,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
        response: Response,
        key: TokenKeyType | None = None,
    ) -> None:
        if key is None:
            access_token_delete_result = access_token.delete(response)
            refresh_token_delete_result = refresh_token.delete(response)
        else:
            access_token_delete_result = access_token.delete_by_key(key)
            refresh_token_delete_result = refresh_token.delete_by_key(key)

        if asyncio.iscoroutine(access_token_delete_result):
            await access_token_delete_result
        if asyncio.iscoroutine(refresh_token_delete_result):
            await refresh_token_delete_result

    @final
    @classmethod
    @override
    async def save_tokens[TokenType](
        cls,
        access_token: SyncOrAsyncAuthTokenType[
            TokenType,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
        refresh_token: SyncOrAsyncAuthTokenType[
            TokenType,
            TokenKeyType,
            PayloadType,
            TokenConfigType,
        ],
        response: Response,
        payload: PayloadType | None,
    ) -> None:
        access_token_save_result = access_token.save(response, payload)
        refresh_token_save_result = refresh_token.save(response, payload)

        if asyncio.iscoroutine(access_token_save_result):
            await access_token_save_result
        if asyncio.iscoroutine(refresh_token_save_result):
            await refresh_token_save_result
