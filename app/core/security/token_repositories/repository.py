import asyncio
from typing import override

from fastapi import Response

from app.core.security.token_repositories.base import BaseTokensRepository
from app.core.security.token_schemas import Payload, TokenBaseModel
from app.core.security.tokens import BaseAsyncToken, BaseSyncToken


class TokensRepository[K](BaseTokensRepository[K, Payload]):
    @classmethod
    @override
    async def _create_tokens[T](
        cls,
        access_token: BaseSyncToken[T, K, Payload] | BaseAsyncToken[T, K, Payload],
        refresh_token: BaseSyncToken[T, K, Payload] | BaseAsyncToken[T, K, Payload],
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

    @classmethod
    @override
    async def _read_token[T](
        cls,
        token: BaseSyncToken[T, K, Payload] | BaseAsyncToken[T, K, Payload],
    ) -> Payload:
        token_read_result = token.read()

        if asyncio.iscoroutine(token_read_result):
            payload = await token_read_result
        else:
            payload = token_read_result

        return payload

    @classmethod
    @override
    async def _update_tokens[T](
        cls,
        access_token: BaseSyncToken[T, K, Payload] | BaseAsyncToken[T, K, Payload],
        refresh_token: BaseSyncToken[T, K, Payload] | BaseAsyncToken[T, K, Payload],
        response: Response,
        payload: Payload,
    ) -> None:
        access_token_update_result = access_token.update(response, payload)
        refresh_token_update_result = refresh_token.update(response, payload)

        if asyncio.iscoroutine(access_token_update_result):
            await access_token_update_result
        if asyncio.iscoroutine(refresh_token_update_result):
            await refresh_token_update_result

    @classmethod
    @override
    async def _delete_tokens[T](
        cls,
        access_token: BaseSyncToken[T, K, Payload] | BaseAsyncToken[T, K, Payload],
        refresh_token: BaseSyncToken[T, K, Payload] | BaseAsyncToken[T, K, Payload],
        response: Response,
        key: K | None = None,
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

    @classmethod
    @override
    async def _save_tokens[T](
        cls,
        access_token: BaseSyncToken[T, K, Payload] | BaseAsyncToken[T, K, Payload],
        refresh_token: BaseSyncToken[T, K, Payload] | BaseAsyncToken[T, K, Payload],
        response: Response,
        payload: Payload | None,
    ) -> None:
        access_token_save_result = access_token.save(response, payload)
        refresh_token_save_result = refresh_token.save(response, payload)

        if asyncio.iscoroutine(access_token_save_result):
            await access_token_save_result
        if asyncio.iscoroutine(refresh_token_save_result):
            await refresh_token_save_result

    @classmethod
    @override
    async def _is_user_initiator(
        cls,
        payload_initiator: Payload,
        key: K,
    ) -> bool:
        return key == payload_initiator.user_id
