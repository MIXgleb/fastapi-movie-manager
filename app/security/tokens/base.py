from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    ClassVar,
    final,
)

import jwt
from fastapi import (
    Response,
)

import app.core.exceptions as exc
from app.core import (
    settings,
)

type TypeJWToken = str
type TypeDictAnyAny = dict[Any, Any]


class BaseToken[Token](ABC):
    __slots__ = ("_token",)

    _token_context: ClassVar

    def __init__(
        self,
        token: Token | None = None,
    ) -> None:
        self._token = token

    @final
    @property
    def token(self) -> Token:
        """Check and get a token.

        Returns
        -------
        Token
            token value

        Raises
        ------
        InvalidTokenError
            token does not exist
        """
        if self._token is None:
            raise exc.InvalidTokenError

        return self._token

    @final
    @token.setter
    def token(
        self,
        new_value: Token,
    ) -> None:
        self._token = new_value

    @final
    @token.deleter
    def token(self) -> None:
        self._token = None


class BaseSyncToken[
    Token,
    TokenKey,
    Payload,
](BaseToken[Token]):
    @abstractmethod
    def create(
        self,
        payload: Payload,
    ) -> Token:
        """Create a token.

        Parameters
        ----------
        payload : Payload
            payload data

        Returns
        -------
        Token
            created token
        """
        raise NotImplementedError

    @abstractmethod
    def read(self) -> Payload:
        """Read and process a token.

        Read and check the expiration of a token.

        Returns
        -------
        Payload
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        response: Response,
        payload: Payload,
    ) -> None:
        """Update a token.

        Parameters
        ----------
        response : Response
            response to the client

        payload : Payload
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        response: Response,
    ) -> None:
        """Delete a token.

        Parameters
        ----------
        response : Response
            response to the client
        """
        raise NotImplementedError

    @abstractmethod
    def delete_by_key(
        self,
        key: TokenKey,
    ) -> None:
        """Delete a token by key.

        Parameters
        ----------
        key : KeyToken
            unique key
        """
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        response: Response,
        _payload: Payload | None,
    ) -> None:
        """Save a token.

        Parameters
        ----------
        response : Response
            response to the client

        payload : Payload | None
            payload data
        """
        raise NotImplementedError


class BaseAsyncToken[
    Token,
    TokenKey,
    Payload,
](BaseToken[Token]):
    @abstractmethod
    async def create(
        self,
        payload: Payload,
    ) -> Token:
        """Create a token.

        Parameters
        ----------
        payload : Payload
            payload data

        Returns
        -------
        Token
            created token
        """
        raise NotImplementedError

    @abstractmethod
    async def read(self) -> Payload:
        """Read and process a token.

        Read and check the expiration of a token.

        Returns
        -------
        Payload
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        response: Response,
        payload: Payload,
    ) -> None:
        """Update a token.

        Parameters
        ----------
        response : Response
            response to the client

        payload : Payload
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        response: Response,
    ) -> None:
        """Delete a token.

        Parameters
        ----------
        response : Response
            response to the client
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_by_key(
        self,
        key: TokenKey,
    ) -> None:
        """Delete a token by key.

        Parameters
        ----------
        key : KeyToken
            unique key
        """
        raise NotImplementedError

    @abstractmethod
    async def save(
        self,
        response: Response,
        _payload: Payload | None,
    ) -> None:
        """Save a token.

        Parameters
        ----------
        response : Response
            response to the client

        payload : Payload | None
            payload data
        """
        raise NotImplementedError


class BaseJWToken[Token](BaseToken[Token]):
    @final
    @classmethod
    def _encrypt_jwtoken(
        cls,
        dict_payload: TypeDictAnyAny,
    ) -> TypeJWToken:
        return jwt.encode(
            payload=dict_payload,
            key=settings.token.secret_jwt_key,
            algorithm=settings.token.algorithm,
        )

    @final
    @classmethod
    def _decrypt_jwtoken(
        cls,
        jwtoken: TypeJWToken,
    ) -> TypeDictAnyAny:
        return jwt.decode(
            jwt=jwtoken,
            key=settings.token.secret_jwt_key,
            algorithms=[settings.token.algorithm],
        )
