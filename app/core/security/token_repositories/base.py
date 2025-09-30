from abc import ABC, abstractmethod

from fastapi import Response
from pydantic import BaseModel

from app.core.security.tokens import BaseAsyncToken, BaseSyncToken


class BaseTokensRepository[K, P](ABC):
    @classmethod
    @abstractmethod
    async def _create_tokens[T](
        cls,
        access_token: BaseSyncToken[T, K, P] | BaseAsyncToken[T, K, P],
        refresh_token: BaseSyncToken[T, K, P] | BaseAsyncToken[T, K, P],
        payload: P,
    ) -> BaseModel:
        """Create all tokens.

        Parameters
        ----------
        access_token : BaseSyncToken | BaseAsyncToken
            access token instance

        refresh_token : BaseSyncToken | BaseAsyncToken
            refresh token instance

        payload : Payload
            payload data

        Returns
        -------
        BaseModel
            created tokens
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def _read_token[T](
        cls,
        token: BaseSyncToken[T, K, P] | BaseAsyncToken[T, K, P],
    ) -> P:
        """Read all tokens.

        Parameters
        ----------
        token : BaseSyncToken | BaseAsyncToken
            token instance

        Returns
        -------
        Payload
            payload data
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def _update_tokens[T](
        cls,
        access_token: BaseSyncToken[T, K, P] | BaseAsyncToken[T, K, P],
        refresh_token: BaseSyncToken[T, K, P] | BaseAsyncToken[T, K, P],
        response: Response,
        payload: P,
    ) -> None:
        """Update all tokens.

        Parameters
        ----------
        access_token : BaseSyncToken | BaseAsyncToken
            access token instance

        refresh_token : BaseSyncToken | BaseAsyncToken
            refresh token instance

        response : Response
            response from the endpoint

        payload : Payload
            payload data
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def _delete_tokens[T](
        cls,
        access_token: BaseSyncToken[T, K, P] | BaseAsyncToken[T, K, P],
        refresh_token: BaseSyncToken[T, K, P] | BaseAsyncToken[T, K, P],
        response: Response,
        key: K | None = None,
    ) -> None:
        """Delete tokens.

        Parameters
        ----------
        access_token : BaseSyncToken | BaseAsyncToken
            access token instance

        refresh_token : BaseSyncToken | BaseAsyncToken
            refresh token instance

        response : Response
            response from the endpoint

        key : TokenKey | None, optional
            unique key, by default None
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def _save_tokens[T](
        cls,
        access_token: BaseSyncToken[T, K, P] | BaseAsyncToken[T, K, P],
        refresh_token: BaseSyncToken[T, K, P] | BaseAsyncToken[T, K, P],
        response: Response,
        payload: P | None,
    ) -> None:
        """Save tokens.

        Parameters
        ----------
        access_token : BaseSyncToken | BaseAsyncToken
            access token instance

        refresh_token : BaseSyncToken | BaseAsyncToken
            refresh token instance

        response : Response
            response from the endpoint

        payload : Payload
            payload data
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def _is_user_initiator[T](
        cls,
        payload_initiator: P,
        key: K,
    ) -> bool:
        """Check if the user is the initiator.

        Parameters
        ----------
        payload_initiator : Payload
            payload data

        key : TokenKey
            unique key

        Returns
        -------
        bool
            verification status
        """
        raise NotImplementedError
