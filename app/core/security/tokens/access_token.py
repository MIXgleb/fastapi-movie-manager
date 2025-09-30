from typing import Any, final, override

import jwt

import app.core.exceptions as exc
from app.core.config import settings
from app.core.security.token_schemas import Payload, Token, TokenPayload
from app.core.security.tokens.base_token import SyncTokenBase, TokenBase

type JWToken = str
type DictAny = dict[Any, Any]


class AccessJWTokenBase(TokenBase[JWToken]):
    _token_context = jwt

    def _encrypt_jwtoken(self, dict_payload: DictAny) -> JWToken:
        return self._token_context.encode(
            payload=dict_payload,
            key=settings.token.secret_key,
            algorithm=settings.token.algorithm,
        )

    def _decrypt_jwtoken(self) -> DictAny:
        return self._token_context.decode(
            jwt=self._get_token(),
            key=settings.token.secret_key,
            algorithms=[settings.token.algorithm],
        )


@final
class AccessJWToken(SyncTokenBase[JWToken], AccessJWTokenBase):
    @override
    def create(self, payload: Payload) -> JWToken:
        token_payload = TokenPayload(
            **payload.model_dump(),
            token_type=Token.access_token,
        )
        self.token = self._encrypt_jwtoken(token_payload.model_dump())
        return self.token

    @override
    def read(self) -> Payload:
        try:
            dict_payload = self._decrypt_jwtoken()
        except jwt.ExpiredSignatureError:
            raise exc.TokenExpiredError from None
        except jwt.InvalidTokenError:
            raise exc.InvalidTokenError from None
        else:
            return Payload(**dict_payload)

    @override
    def update(self, payload: Payload) -> None:
        self.token = self.create(payload)
        self.save()

    @override
    def delete(self) -> None:
        self.response.delete_cookie(Token.access_token)
        self.token = None

    @override
    def save(self) -> None:
        self.response.set_cookie(
            key=Token.access_token,
            value=self._get_token(),
            max_age=settings.token.access_token_ttl_seconds,
            httponly=True,
        )
