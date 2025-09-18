from abc import ABC, abstractmethod
from typing import Annotated, override

import jwt
from fastapi import Cookie, Response

import app.core.exceptions as exc
from app.core.config import settings
from app.schemas import Payload, Role, Token, TokensCreate, TokensRead


class TokenHelperBase[Tokens, Create, Return](ABC):
    async def __call__(self, tokens: Tokens, response: Response) -> Payload:
        """Get and process a token.

        Check the expiration of a token.

        Parameters
        ----------
        tokens : Tokens
            client's tokens

        response : Response
            response to the client

        Returns
        -------
        Payload
            payload data
        """
        return self.check(tokens, response)

    @abstractmethod
    def check(self, tokens: Tokens, response: Response) -> Payload:
        """Get and process a token.

        Check the expiration of a token.

        Parameters
        ----------
        tokens : Tokens
            client's tokens

        response : Response
            response to the client

        Returns
        -------
        Payload
            payload data
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(cls, payload: Payload) -> Return:
        """Create a token.

        Parameters
        ----------
        payload : Payload
            payload data

        Returns
        -------
        Return
            token
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def install(cls, tokens: Create, response: Response) -> None:
        """Install a token for the client.

        Parameters
        ----------
        tokens : Create
            new tokens

        response : Response
            response to the client
        """
        raise NotImplementedError


class JWTTokenHelper(TokenHelperBase[TokensRead, TokensCreate, str]):
    @override
    async def __call__(
        self,
        tokens: Annotated[TokensRead, Cookie()],
        response: Response,
    ) -> Payload:
        return await super().__call__(tokens, response)

    @classmethod
    def _update_tokens(cls, response: Response, payload: Payload) -> str:
        new_access_token = cls.create(
            Payload(
                user_id=payload.user_id,
                user_role=payload.user_role,
                token_type=Token.access_token,
            )
        )
        new_refresh_token = cls.create(
            Payload(
                user_id=payload.user_id,
                user_role=payload.user_role,
                token_type=Token.refresh_token,
            )
        )
        new_tokens = TokensCreate(access_token=new_access_token, refresh_token=new_refresh_token)
        cls.install(new_tokens, response)
        return new_access_token

    @classmethod
    def _decode(cls, token: str) -> Payload:
        try:
            payload_data = jwt.decode(  # type: ignore[reportUnknownMemberType]
                jwt=token,
                key=settings.token.secret_key,
                algorithms=[settings.token.algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise exc.TokenExpiredError from None
        except jwt.InvalidTokenError:
            raise exc.InvalidTokenError from None
        else:
            return Payload(**payload_data)

    @override
    def check(self, tokens: TokensRead, response: Response) -> Payload:
        if tokens.access_token is None:
            if tokens.refresh_token is None:
                return Payload(user_id=0, user_role=Role.guest, token_type=Token.guest_token)

            payload = self._decode(tokens.refresh_token)
            return self._decode(self._update_tokens(response, payload))

        return self._decode(tokens.access_token)

    @classmethod
    @override
    def create(cls, payload: Payload) -> str:
        return jwt.encode(  # type: ignore[reportUnknownMemberType]
            payload=payload.model_dump(),
            key=settings.token.secret_key,
            algorithm=settings.token.algorithm,
        )

    @classmethod
    @override
    def install(cls, tokens: TokensCreate, response: Response) -> None:
        response.set_cookie(
            key=Token.access_token,
            value=tokens.access_token,
            max_age=settings.token.access_token_expiration,
            httponly=True,
        )
        response.set_cookie(
            key=Token.refresh_token,
            value=tokens.refresh_token,
            max_age=settings.token.refresh_token_expiration,
            httponly=True,
        )
