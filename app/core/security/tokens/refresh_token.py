from abc import abstractmethod
from typing import Any, ClassVar, final, override

import jwt
import redis.asyncio as redis
from cryptography.fernet import Fernet

import app.core.exceptions as exc
from app.core.config import settings
from app.core.security.token_schemas import Payload, Token, TokenPayload
from app.core.security.tokens.base_token import AsyncTokenBase, TokenBase

type JWToken = str
type EncryptedUserID = str
type DictAny = dict[Any, Any]


class RefreshJWTokenBase(TokenBase[EncryptedUserID]):
    _redis: ClassVar[redis.Redis] = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db_refresh_token,
        encoding=settings.redis.encoding,
        decode_responses=True,
    )
    _token_context = Fernet(settings.token.secret_key)

    def _encrypt_user_id(self, user_id: int) -> EncryptedUserID:
        return self._token_context.encrypt(str(user_id).encode()).decode()

    def _decrypt_user_id(self) -> int:
        return int(self._token_context.decrypt(self._get_token().encode()).decode())

    @classmethod
    def _encrypt_jwtoken(cls, dict_payload: DictAny) -> JWToken:
        return jwt.encode(
            payload=dict_payload,
            key=settings.token.secret_key,
            algorithm=settings.token.algorithm,
        )

    @classmethod
    def _decrypt_jwtoken(cls, jwtoken: JWToken) -> DictAny:
        return jwt.decode(
            jwt=jwtoken,
            key=settings.token.secret_key,
            algorithms=[settings.token.algorithm],
        )

    @abstractmethod
    async def delete_by_user_id(self, user_id: int) -> None:
        """Delete a token by user id.

        Parameters
        ----------
        user_id : int
            user id
        """
        raise NotImplementedError


@final
class RefreshJWToken(AsyncTokenBase[EncryptedUserID], RefreshJWTokenBase):
    @override
    async def create(self, payload: Payload) -> EncryptedUserID:
        token_payload = TokenPayload(
            **payload.model_dump(),
            token_type=Token.refresh_token,
        )
        jwtoken = self._encrypt_jwtoken(token_payload.model_dump())
        self.token = self._encrypt_user_id(payload.user_id)
        await self._redis.setex(
            name=self.token,
            time=settings.token.refresh_token_ttl,
            value=jwtoken,
        )
        return self.token

    @override
    async def read(self) -> Payload:
        jwtoken = await self._redis.get(self._get_token())

        if jwtoken is None:
            raise exc.TokenExpiredError from None

        try:
            dict_payload = self._decrypt_jwtoken(jwtoken)
        except jwt.ExpiredSignatureError:
            raise exc.TokenExpiredError from None
        except jwt.InvalidTokenError:
            raise exc.InvalidTokenError from None
        else:
            return Payload(**dict_payload)

    @override
    async def update(self, payload: Payload) -> None:
        self.token = await self.create(payload)
        await self.save()

    @override
    async def delete(self) -> None:
        await self._redis.delete(self._get_token())
        self.response.delete_cookie(Token.refresh_token)
        self.token = None

    @override
    async def save(self) -> None:
        self.response.set_cookie(
            key=Token.refresh_token,
            value=self._get_token(),
            max_age=settings.token.refresh_token_ttl_seconds,
            httponly=True,
        )

    @override
    async def delete_by_user_id(self, user_id: int) -> None:
        encrypted_user_id = self._encrypt_user_id(user_id)
        await self._redis.delete(encrypted_user_id)
