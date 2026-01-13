import asyncio
from abc import ABC, abstractmethod
from typing import Any, final, override

from fastapi import Response

from app.security.token_schemas import TokenBaseModel
from app.security.tokens import BaseAsyncToken, BaseSyncToken, BaseToken

type TypeSyncOrAsyncToken[Token, TokenKey, Payload] = (
    BaseSyncToken[Token, TokenKey, Payload] | BaseAsyncToken[Token, TokenKey, Payload]
)


class BaseTokenRepository[
    TokenKey,
    Payload,
    TokenType: BaseToken[Any],
](ABC):
    @classmethod
    @abstractmethod
    async def create_tokens(
        cls,
        access_token: TokenType,
        refresh_token: TokenType,
        payload: Payload,
    ) -> TokenBaseModel:
        """Create all tokens.

        Parameters
        ----------
        access_token : BaseToken
            access token instance

        refresh_token : BaseToken
            refresh token instance

        payload : Payload
            payload data

        Returns
        -------
        TokenBaseModel
            created tokens
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def read_token(
        cls,
        token: TokenType,
    ) -> Payload:
        """Read all tokens.

        Parameters
        ----------
        token : BaseToken
            token instance

        Returns
        -------
        P
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
        payload: Payload,
    ) -> None:
        """Update all tokens.

        Parameters
        ----------
        access_token : BaseToken
            access token instance

        refresh_token : BaseToken
            refresh token instance

        response : Response
            response to the client

        payload : Payload
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
        key: TokenKey | None = None,
    ) -> None:
        """Delete tokens.

        Parameters
        ----------
        access_token : BaseToken
            access token instance

        refresh_token : BaseToken
            refresh token instance

        response : Response
            response to the client

        key : TokenKey | None, optional
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
        payload: Payload | None,
    ) -> None:
        """Save tokens.

        Parameters
        ----------
        access_token : BaseToken
            access token instance

        refresh_token : BaseToken
            refresh token instance

        response : Response
            response to the client

        payload : Payload | None
            payload data
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def is_user_initiator(
        cls,
        payload_initiator: Payload,
        key: TokenKey,
    ) -> bool:
        """Check if the user is the initiator.

        Parameters
        ----------
        payload_initiator : Payload
            payload data

        key : TokenKey
            unique key

        Returns
        -------
        bool
            verification status
        """
        raise NotImplementedError


class BaseSyncAsyncTokenRepository[
    TokenKey,
    Payload,
](
    BaseTokenRepository[
        TokenKey,
        Payload,
        TypeSyncOrAsyncToken[Any, TokenKey, Payload],
    ],
):
    @final
    @classmethod
    @override
    async def create_tokens[Token](
        cls,
        access_token: TypeSyncOrAsyncToken[Token, TokenKey, Payload],
        refresh_token: TypeSyncOrAsyncToken[Token, TokenKey, Payload],
        payload: Payload,
    ) -> TokenBaseModel:
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

        return TokenBaseModel(
            access_token=access_token_value,
            refresh_token=refresh_token_value,
        )

    @final
    @classmethod
    @override
    async def read_token[Token](
        cls,
        token: TypeSyncOrAsyncToken[Token, TokenKey, Payload],
    ) -> Payload:
        token_read_result = token.read()

        if asyncio.iscoroutine(token_read_result):
            payload: Payload = await token_read_result
        else:
            payload: Payload = token_read_result

        return payload

    @final
    @classmethod
    @override
    async def update_tokens[Token](
        cls,
        access_token: TypeSyncOrAsyncToken[Token, TokenKey, Payload],
        refresh_token: TypeSyncOrAsyncToken[Token, TokenKey, Payload],
        response: Response,
        payload: Payload,
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
    async def delete_tokens[Token](
        cls,
        access_token: TypeSyncOrAsyncToken[Token, TokenKey, Payload],
        refresh_token: TypeSyncOrAsyncToken[Token, TokenKey, Payload],
        response: Response,
        key: TokenKey | None = None,
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
    async def save_tokens[Token](
        cls,
        access_token: TypeSyncOrAsyncToken[Token, TokenKey, Payload],
        refresh_token: TypeSyncOrAsyncToken[Token, TokenKey, Payload],
        response: Response,
        payload: Payload | None,
    ) -> None:
        access_token_save_result = access_token.save(response, payload)
        refresh_token_save_result = refresh_token.save(response, payload)

        if asyncio.iscoroutine(access_token_save_result):
            await access_token_save_result
        if asyncio.iscoroutine(refresh_token_save_result):
            await refresh_token_save_result
