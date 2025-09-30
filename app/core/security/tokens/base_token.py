from abc import ABC, abstractmethod
from typing import ClassVar

from fastapi import Response

import app.core.exceptions as exc
from app.core.security.token_schemas import Payload


class TokenBase[Token](ABC):
    __slots__ = ("response", "token")

    _token_context: ClassVar

    def __init__(
        self,
        response: Response,
        token: Token | None = None,
    ) -> None:
        self.response = response
        self.token: Token | None = token

    def _get_token(self) -> Token:
        if self.token is None:
            raise exc.InvalidTokenError

        return self.token


class SyncTokenBase[Token](
    TokenBase[Token],
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
    def update(self, payload: Payload) -> None:
        """Update a token.

        Parameters
        ----------
        payload : Payload
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        """Delete a token."""
        raise NotImplementedError

    @abstractmethod
    def save(self) -> None:
        """Save a token."""
        raise NotImplementedError


class AsyncTokenBase[Token](
    TokenBase[Token],
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
    async def update(self, payload: Payload) -> None:
        """Update a token.

        Parameters
        ----------
        payload : Payload
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self) -> None:
        """Delete a token."""
        raise NotImplementedError

    @abstractmethod
    async def save(self) -> None:
        """Save a token."""
        raise NotImplementedError
