from abc import (
    abstractmethod,
)
from typing import (
    final,
    override,
)
from uuid import (
    UUID,
)

import jwt
from fastapi import (
    Response,
)

import app.core.exceptions as exc
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
    BaseAuthJWT,
    BaseSyncAuthToken,
    JWTokenType,
)


class BaseAuthAccessToken[
    TokenType,
    TokenKeyType,
    PayloadType: BasePayload,
](
    BaseSyncAuthToken[
        TokenType,
        TokenKeyType,
        PayloadType,
        AuthTokenConfig,
    ],
):
    """Basic abstract auth access token class."""

    @override
    @abstractmethod
    def save(
        self,
        response: Response,
        payload: PayloadType | None = None,
    ) -> None:
        """
        Save a token.

        Parameters
        ----------
        response : Response
            response to the client

        payload : PayloadType | None, optional
            payload data, by default None
        """
        raise NotImplementedError


@final
class AuthAccessJWT(
    BaseAuthJWT[JWTokenType],
    BaseAuthAccessToken[
        JWTokenType,
        int | UUID,
        Payload,
    ],
):
    """Sync auth access jwt."""

    @override
    def create(
        self,
        payload: Payload,
    ) -> JWTokenType:
        token_payload = JWTPayload(
            **payload.model_dump(),
            token_type=TokenKey.ACCESS_TOKEN,
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
        response.delete_cookie(TokenKey.ACCESS_TOKEN)
        del self.token

    @override
    def delete_by_key(
        self,
        key: int | UUID,
    ) -> None:
        pass

    @override
    def save(
        self,
        response: Response,
        payload: Payload | None = None,
    ) -> None:
        response.set_cookie(
            key=TokenKey.ACCESS_TOKEN,
            value=self.token,
            max_age=self.token_config.access_token_ttl_seconds.get_secret_value(),
            httponly=True,
        )
