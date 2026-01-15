from typing import ClassVar, final, override

import jwt
import redis.asyncio as redis
from cryptography.fernet import Fernet
from fastapi import Response

import app.core.exceptions as exc
from app.core import settings
from app.security.token_schemas import JWTokenPayload, Payload, TokenKey
from app.security.tokens.base import BaseAsyncToken, BaseJWToken

type TypeEncryptedUserID = str


class BaseRefreshJWToken(BaseJWToken[TypeEncryptedUserID]):
    _redis: ClassVar[redis.Redis] = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db_refresh_token,
        encoding=settings.redis.encoding,
        decode_responses=True,
    )
    _token_context = Fernet(settings.token.secret_fernet_key)

    @final
    def _encrypt_user_id(
        self,
        user_id: int,
    ) -> TypeEncryptedUserID:
        encoded_user_id = str(user_id).encode()
        return self._token_context.encrypt(encoded_user_id).decode()

    @final
    def _decrypt_user_id(self) -> int:
        encoded_token = self.token.encode()
        return int(self._token_context.decrypt(encoded_token).decode())


@final
class RefreshJWToken(
    BaseAsyncToken[
        TypeEncryptedUserID,
        int,
        Payload,
    ],
    BaseRefreshJWToken,
):
    @override
    async def create(
        self,
        payload: Payload,
    ) -> TypeEncryptedUserID:
        self.token = self._encrypt_user_id(payload.user_id)
        return self.token

    @override
    async def read(self) -> Payload:
        jwtoken = await self._redis.get(self.token)

        if jwtoken is None:
            raise exc.ExpiredTokenError from None

        try:
            dict_payload = self._decrypt_jwtoken(jwtoken)
        except jwt.ExpiredSignatureError:
            raise exc.ExpiredTokenError from None
        except jwt.InvalidTokenError:
            raise exc.InvalidTokenError from None
        else:
            return Payload(**dict_payload)

    @override
    async def update(
        self,
        response: Response,
        payload: Payload,
    ) -> None:
        await self.delete(response)
        await self.create(payload)
        await self.save(response, payload)

    @override
    async def delete(
        self,
        response: Response,
    ) -> None:
        if self._token is not None:
            await self._redis.delete(self.token)

        response.delete_cookie(TokenKey.refresh_token)
        del self.token

    @override
    async def delete_by_key(
        self,
        key: int,
    ) -> None:
        encrypted_user_id = self._encrypt_user_id(key)
        await self._redis.delete(encrypted_user_id)

    @override
    async def save(
        self,
        response: Response,
        payload: Payload | None,
    ) -> None:
        if payload is None:
            msg_err = (
                f"{self.__class__.__name__}.save() missing 1 required "
                "positional argument: 'payload'"
            )
            raise TypeError(msg_err)

        token_payload = JWTokenPayload(
            **payload.model_dump(),
            token_type=TokenKey.refresh_token,
        )
        jwtoken = self._encrypt_jwtoken(token_payload.model_dump())

        await self._redis.setex(
            name=self.token,
            time=settings.token.refresh_token_ttl,
            value=jwtoken,
        )
        response.set_cookie(
            key=TokenKey.refresh_token,
            value=self.token,
            max_age=settings.token.refresh_token_ttl_seconds,
            httponly=True,
        )
