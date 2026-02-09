from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
)

from fastapi import (
    Request,
    Response,
)

from app.security.token_repositories import (
    BaseTokenRepository,
)
from app.security.token_schemas import (
    TokenBaseModel,
)
from app.security.tokens import (
    BaseToken,
)


class BaseTokenHelper[
    TokenKey,
    Payload,
    TokenType: BaseToken[Any],
    Tokens: TokenBaseModel,
](ABC):
    tokens: BaseTokenRepository[
        TokenKey,
        Payload,
        TokenType,
    ]

    @classmethod
    @abstractmethod
    async def store_payload(
        cls,
        tokens: Tokens,
        request: Request,
    ) -> None:
        """Get the payload from the tokens and store it to the request state.

        Parameters
        ----------
        tokens : TokenBaseModel
            client's tokens

        request : Request
            request from the client

        Raises
        ------
        InvalidTokenError
            token does not exist
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def store_tokens(
        cls,
        tokens: Tokens,
        request: Request,
    ) -> None:
        """Store tokens to the request state.

        Parameters
        ----------
        tokens : TokenBaseModel
            client's tokens

        request : Request
            request from the client
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def check_admin_rights(
        cls,
        request: Request,
    ) -> None:
        """Check the admin rights.

        Parameters
        ----------
        request : Request
            request from the client

        Raises
        ------
        UserPermissionError
            access is forbidden
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def validate_tokens(
        cls,
        request: Request,
    ) -> Tokens:
        """Validate the client's tokens.

        Parameters
        ----------
        request : Request
            request from the client

        Returns
        -------
        TokenBaseModel
            received tokens

        Raises
        ------
        InvalidTokenError
            token does not exist
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def generate_tokens(
        cls,
        payload: Payload,
        request: Request,
    ) -> None:
        """Generate all tokens.

        Parameters
        ----------
        payload : Payload
            payload data

        request : Request
            request from the client
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def update_tokens(
        cls,
        updated_payload: Payload,
        request: Request,
        response: Response,
    ) -> None:
        """Update all tokens.

        Parameters
        ----------
        updated_payload : Payload
            updated payload data

        request : Request
            request from the client

        response : Response
            response to the client
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def clear_tokens(
        cls,
        request: Request,
        response: Response,
        user_id: int | None = None,
    ) -> None:
        """Clear all tokens.

        Parameters
        ----------
        request : Request
            request from the client

        response : Response
            response to the client

        user_id : int | None, optional
            user id, by default None
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def save_tokens(
        cls,
        request: Request,
        response: Response,
    ) -> None:
        """Save tokens in cookie.

        Parameters
        ----------
        request : Request
            request from the client

        response : Response
            response to the client
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def payload_getter(
        cls,
        request: Request,
    ) -> Payload:
        """Get a payload data.

        Parameters
        ----------
        request : Request
            request from the client

        Returns
        -------
        Payload
            stored payload data
        """
        raise NotImplementedError
