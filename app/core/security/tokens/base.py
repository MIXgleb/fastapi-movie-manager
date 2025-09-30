from abc import ABC, abstractmethod
from typing import ClassVar

from fastapi import Response

import app.core.exceptions as exc


class BaseToken[Token](ABC):
    __slots__ = ("_token",)

    _token_context: ClassVar

    def __init__(self, token: Token | None = None) -> None:
        self._token = token

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

    @token.setter
    def token(self, new_value: Token) -> None:
        self._token = new_value

    @token.deleter
    def token(self) -> None:
        self._token = None


class BaseSyncToken[Token, TokenKey, Payload](
    BaseToken[Token],
):
    @abstractmethod
    def create(self, payload: Payload) -> Token:
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
    def update(self, response: Response, payload: Payload) -> None:
        """Update a token.

        Parameters
        ----------
        response : Response
            response from the endpoint

        payload : Payload
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, response: Response) -> None:
        """Delete a token.

        Parameters
        ----------
        response : Response
            response from the endpoint
        """
        raise NotImplementedError

    @abstractmethod
    def delete_by_key(self, key: TokenKey) -> None:
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
            response from the endpoint

        payload : Payload | None
            payload data
        """
        raise NotImplementedError


class BaseAsyncToken[Token, TokenKey, Payload](
    BaseToken[Token],
):
    @abstractmethod
    async def create(self, payload: Payload) -> Token:
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
    async def update(self, response: Response, payload: Payload) -> None:
        """Update a token.

        Parameters
        ----------
        response : Response
            response from the endpoint

        payload : Payload
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, response: Response) -> None:
        """Delete a token.

        Parameters
        ----------
        response : Response
            response from the endpoint
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_by_key(self, key: TokenKey) -> None:
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
            response from the endpoint

        payload : Payload | None
            payload data
        """
        raise NotImplementedError
