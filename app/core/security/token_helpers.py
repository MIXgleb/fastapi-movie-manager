import asyncio
from abc import ABC, abstractmethod
from typing import Annotated, override

from fastapi import Cookie, Response

from app.core.security.token_schemas import (
    JWTokenReadDTO,
    Payload,
    TokenBase,
    UserRole,
)
from app.core.security.tokens import (
    AccessJWToken,
    AsyncTokenBase,
    RefreshJWToken,
    SyncTokenBase,
)

TokensFromCookie = Annotated[JWTokenReadDTO, Cookie()]


class TokenHelperBase[Tokens: TokenBase](ABC):
    @abstractmethod
    async def __call__(
        self,
        tokens: Tokens,
        response: Response,
    ) -> Payload:
        """Check the client's tokens.

        Parameters
        ----------
        tokens : Tokens
            client's tokens

        response : Response
            response from the endpoint

        Returns
        -------
        Payload
            payload data
        """
        raise NotImplementedError

    @classmethod
    async def _create_tokens[T](
        cls,
        access_token: SyncTokenBase[T] | AsyncTokenBase[T],
        refresh_token: SyncTokenBase[T] | AsyncTokenBase[T],
        payload: Payload,
    ) -> None:
        """Create all tokens.

        Parameters
        ----------
        access_token : SyncTokenBase | AsyncTokenBase
            access token instance

        refresh_token : SyncTokenBase | AsyncTokenBase
            refresh token instance

        payload : Payload
            payload data
        """
        access_token_create_result = access_token.create(payload)
        refresh_token_create_result = refresh_token.create(payload)

        if asyncio.iscoroutine(access_token_create_result):
            await access_token_create_result
        if asyncio.iscoroutine(refresh_token_create_result):
            await refresh_token_create_result

    @classmethod
    async def _read_token[T](
        cls,
        token: SyncTokenBase[T] | AsyncTokenBase[T],
    ) -> Payload:
        """Read all tokens.

        Parameters
        ----------
        token : SyncTokenBase | AsyncTokenBase
            token instance

        Returns
        -------
        Payload
            payload data
        """
        token_read_result = token.read()

        if asyncio.iscoroutine(token_read_result):
            payload = await token_read_result
        else:
            payload = token_read_result

        return payload

    @classmethod
    async def _update_tokens[T](
        cls,
        access_token: SyncTokenBase[T] | AsyncTokenBase[T],
        refresh_token: SyncTokenBase[T] | AsyncTokenBase[T],
        payload: Payload,
    ) -> None:
        """Update all tokens.

        Parameters
        ----------
        access_token : SyncTokenBase | AsyncTokenBase
            access token instance

        refresh_token : SyncTokenBase | AsyncTokenBase
            refresh token instance

        payload : Payload
            payload data
        """
        access_token_update_result = access_token.update(payload)
        refresh_token_update_result = refresh_token.update(payload)

        if asyncio.iscoroutine(access_token_update_result):
            await access_token_update_result
        if asyncio.iscoroutine(refresh_token_update_result):
            await refresh_token_update_result

    @classmethod
    async def _delete_tokens[T](
        cls,
        access_token: SyncTokenBase[T] | AsyncTokenBase[T],
        refresh_token: SyncTokenBase[T] | AsyncTokenBase[T],
    ) -> None:
        """Delete all tokens.

        Parameters
        ----------
        access_token : SyncTokenBase | AsyncTokenBase
            access token instance

        refresh_token : SyncTokenBase | AsyncTokenBase
            refresh token instance
        """
        access_token_delete_result = access_token.delete()
        refresh_token_delete_result = refresh_token.delete()

        if asyncio.iscoroutine(access_token_delete_result):
            await access_token_delete_result
        if asyncio.iscoroutine(refresh_token_delete_result):
            await refresh_token_delete_result

    @classmethod
    async def _save_tokens[T](
        cls,
        access_token: SyncTokenBase[T] | AsyncTokenBase[T],
        refresh_token: SyncTokenBase[T] | AsyncTokenBase[T],
    ) -> None:
        """Save tokens.

        Parameters
        ----------
        access_token : SyncTokenBase | AsyncTokenBase
            access token instance

        refresh_token : SyncTokenBase | AsyncTokenBase
            refresh token instance
        """
        access_token_save_result = access_token.save()
        refresh_token_save_result = refresh_token.save()

        if asyncio.iscoroutine(access_token_save_result):
            await access_token_save_result
        if asyncio.iscoroutine(refresh_token_save_result):
            await refresh_token_save_result

    @classmethod
    async def _is_user_initiator[T](
        cls,
        token: SyncTokenBase[T] | AsyncTokenBase[T],
        user_id: int,
    ) -> bool:
        """Check if the user is the initiator.

        Parameters
        ----------
        token : SyncTokenBase | AsyncTokenBase
            token instance

        user_id : int
            user id

        Returns
        -------
        bool
            verification status
        """
        payload_initiator = await cls._read_token(token)
        return user_id == payload_initiator.user_id


class JWTokenHelper(TokenHelperBase[TokensFromCookie]):
    @override
    async def __call__(
        self,
        tokens: TokensFromCookie,
        response: Response,
    ) -> Payload:
        if tokens.access_token is None:
            if tokens.refresh_token is None:
                return Payload(user_id=0, user_role=UserRole.guest)

            access_token = AccessJWToken(response)
            refresh_token = RefreshJWToken(response, tokens.refresh_token)
            payload = await self._read_token(refresh_token)
            await self._delete_tokens(access_token, refresh_token)
            await self._update_tokens(
                access_token=access_token,
                refresh_token=refresh_token,
                payload=payload,
            )
            return payload

        access_token = AccessJWToken(response, tokens.access_token)
        return await self._read_token(access_token)

    @classmethod
    async def generate_tokens(
        cls,
        response: Response,
        payload: Payload,
    ) -> None:
        """Generate all tokens.

        Parameters
        ----------
        response : Response
            response from the endpoint

        payload : Payload
            payload data
        """
        access_token = AccessJWToken(response)
        refresh_token = RefreshJWToken(response)
        await cls._create_tokens(
            access_token=access_token,
            refresh_token=refresh_token,
            payload=payload,
        )
        await cls._save_tokens(access_token, refresh_token)

    @classmethod
    async def update_tokens(
        cls,
        tokens: JWTokenReadDTO,
        response: Response,
        payload: Payload,
    ) -> None:
        """Update all tokens.

        Parameters
        ----------
        tokens : JWTokenReadDTO
            client's tokens

        response : Response
            response from the endpoint

        payload : Payload
            payload data
        """
        access_token = AccessJWToken(response, tokens.access_token)
        refresh_token = RefreshJWToken(response, tokens.refresh_token)

        if await cls._is_user_initiator(access_token, payload.user_id):
            await cls._delete_tokens(access_token, refresh_token)
            await cls._update_tokens(
                access_token=access_token,
                refresh_token=refresh_token,
                payload=payload,
            )
        else:
            await refresh_token.delete_by_user_id(payload.user_id)

    @classmethod
    async def clear_tokens(
        cls,
        tokens: JWTokenReadDTO,
        response: Response,
        user_id: int | None = None,
    ) -> None:
        """Clear all tokens.

        Parameters
        ----------
        tokens : JWTokenReadDTO
            client's tokens

        response : Response
            response from the endpoint

        user_id : int | None, optional
            user id, by default None
        """
        access_token = AccessJWToken(response, tokens.access_token)
        refresh_token = RefreshJWToken(response, tokens.refresh_token)

        if user_id is None or await cls._is_user_initiator(access_token, user_id):
            await cls._delete_tokens(access_token, refresh_token)
        else:
            await refresh_token.delete_by_user_id(user_id)
