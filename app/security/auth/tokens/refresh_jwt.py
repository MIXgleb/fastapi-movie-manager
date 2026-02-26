from abc import abstractmethod
from typing import (
    ClassVar,
    Literal,
    final,
    overload,
    override,
)
from uuid import (
    UUID,
)

import jwt
import redis.asyncio as redis
from cryptography.fernet import (
    Fernet,
)
from fastapi import (
    Response,
)

import app.core.exceptions as exc
from app.core import (
    settings,
)
from app.core.config import (
    AuthTokenConfig,
)
from app.security.auth.schemas import (
    BasePayload,
    JWTPayload,
    Payload,
    TokenKey,
)
from app.security.auth.tokens.base import (
    BaseAsyncAuthToken,
    BaseAuthJWT,
)

type EncryptedUserIDType = str


class BaseAuthRefreshToken[
    TokenType,
    TokenKeyType,
    PayloadType: BasePayload,
](
    BaseAsyncAuthToken[
        TokenType,
        TokenKeyType,
        PayloadType,
        AuthTokenConfig,
    ],
):
    """Basic abstract auth refresh token class."""

    _redis: ClassVar[redis.Redis] = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db_refresh_token,
        encoding=settings.redis.encoding,
        decode_responses=True,
    )
    _token_context: ClassVar

    @abstractmethod
    def _encrypt_user_id(
        self,
        user_id: TokenKeyType,
    ) -> TokenType:
        raise NotImplementedError

    @abstractmethod
    def _decrypt_user_id(self) -> TokenKeyType:
        raise NotImplementedError


@final
class AuthRefreshJWT(
    BaseAuthJWT[EncryptedUserIDType],
    BaseAuthRefreshToken[
        EncryptedUserIDType,
        int | UUID,
        Payload,
    ],
):
    """Async auth refresh jwt."""

    _token_context: ClassVar[Fernet] = Fernet(
        key=settings.auth_token.secret_fernet_key.get_secret_value(),
    )

    @override
    def _encrypt_user_id(
        self,
        user_id: int | UUID,
    ) -> EncryptedUserIDType:
        encoded_user_id = str(user_id).encode()
        return self._token_context.encrypt(encoded_user_id).decode()

    @overload
    def _decrypt_user_id(self, *, as_uuid: Literal[True]) -> UUID: ...

    @overload
    def _decrypt_user_id(self, *, as_uuid: Literal[False] = False) -> int: ...

    @override
    def _decrypt_user_id(self, *, as_uuid: bool = False) -> int | UUID:
        encoded_token = self.token.encode()
        decrypted_token = self._token_context.decrypt(encoded_token)

        if as_uuid:
            return UUID(bytes=decrypted_token)
        return int(decrypted_token)

    @override
    async def create(
        self,
        payload: Payload,
    ) -> EncryptedUserIDType:
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

        response.delete_cookie(TokenKey.REFRESH_TOKEN)
        del self.token

    @override
    async def delete_by_key(
        self,
        key: int | UUID,
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
            exc_msg = (
                f"{self.__class__.__name__}.save() missing 1 required "
                "positional argument: 'payload'"
            )
            raise TypeError(exc_msg)

        token_payload = JWTPayload(
            **payload.model_dump(),
            token_type=TokenKey.REFRESH_TOKEN,
        )
        jwtoken = self._encrypt_jwtoken(token_payload.model_dump())

        await self._redis.setex(
            name=self.token,
            time=self.token_config.refresh_token_ttl.get_secret_value(),
            value=jwtoken,
        )
        response.set_cookie(
            key=TokenKey.REFRESH_TOKEN,
            value=self.token,
            max_age=self.token_config.refresh_token_ttl_seconds.get_secret_value(),
            httponly=True,
        )
