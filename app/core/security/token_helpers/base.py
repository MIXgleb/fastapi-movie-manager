from abc import ABC, abstractmethod

from fastapi import Request, Response


class BaseTokenHelper[Tokens, Payload](ABC):
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
        tokens : Tokens
            client's tokens

        request : Request
            request to the endpoint

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
        tokens : Tokens
            client's tokens

        request : Request
            request to the endpoint
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def check_admin_rights(cls, request: Request) -> None:
        """Check the admin rights.

        Parameters
        ----------
        request : Request
            request to the endpoint

        Raises
        ------
        UserPermissionError
            access is forbidden
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def validate_tokens(cls, request: Request) -> Tokens:
        """Validate the client's tokens.

        Parameters
        ----------
        request : Request
            request to the endpoint

        Returns
        -------
        Tokens
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
            request to the endpoint
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
            request to the endpoint

        response : Response
            response from the endpoint
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
            request to the endpoint

        response : Response
            response from the endpoint

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
            request to the endpoint

        response : Response
            response from the endpoint
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def payload_getter(cls, request: Request) -> Payload:
        """Get a payload data.

        Parameters
        ----------
        request : Request
            request to the endpoint

        Returns
        -------
        Payload
            stored payload data
        """
        raise NotImplementedError
