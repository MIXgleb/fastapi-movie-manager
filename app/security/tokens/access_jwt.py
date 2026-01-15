from typing import final, override

import jwt
from fastapi import Response

import app.core.exceptions as exc
from app.core import settings
from app.security.token_schemas import JWTokenPayload, Payload, TokenKey
from app.security.tokens.base import BaseJWToken, BaseSyncToken, TypeJWToken


@final
class AccessJWToken(
    BaseSyncToken[
        TypeJWToken,
        int,
        Payload,
    ],
    BaseJWToken[TypeJWToken],
):
    _token_context = jwt

    @override
    def create(
        self,
        payload: Payload,
    ) -> TypeJWToken:
        token_payload = JWTokenPayload(
            **payload.model_dump(),
            token_type=TokenKey.access_token,
        )
        self.token = self._encrypt_jwtoken(token_payload.model_dump())
        return self.token

    @override
    def read(self) -> Payload:
        try:
            dict_payload = self._decrypt_jwtoken(self.token)
        except jwt.ExpiredSignatureError:
            raise exc.ExpiredTokenError from None
        except jwt.InvalidTokenError:
            raise exc.InvalidTokenError from None
        else:
            return Payload(**dict_payload)

    @override
    def update(
        self,
        response: Response,
        payload: Payload,
    ) -> None:
        self.delete(response)
        self.create(payload)
        self.save(response)

    @override
    def delete(
        self,
        response: Response,
    ) -> None:
        response.delete_cookie(TokenKey.access_token)
        del self.token

    @override
    def delete_by_key(
        self,
        key: int,
    ) -> None:
        pass

    @override
    def save(
        self,
        response: Response,
        _payload: Payload | None = None,
    ) -> None:
        response.set_cookie(
            key=TokenKey.access_token,
            value=self.token,
            max_age=settings.token.access_token_ttl_seconds,
            httponly=True,
        )
