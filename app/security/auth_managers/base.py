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
from pydantic import (
    BaseModel as BaseSchema,
)

from app.security.auth import (
    BaseAuthToken,
    BaseAuthTokenDTO,
    BaseAuthTokenRepository,
    BasePayload,
)


class BaseAuthManager[
    TokenKeyType,
    PayloadType: BasePayload,
    TokenType: BaseAuthToken[Any, Any],
    TokenDTOType: BaseAuthTokenDTO,
    AuthConfigType: BaseSchema,
](ABC):
    """Basic abstract auth manager class."""

    __slots__ = ("auth_config",)

    _repo: BaseAuthTokenRepository[
        TokenKeyType,
        PayloadType,
        TokenType,
    ]

    def __init__(
        self,
        auth_config: AuthConfigType,
    ) -> None:
        """
        Initialize the token manager.

        Parameters
        ----------
        auth_config : AuthConfigType
            auth config
        """
        self.auth_config = auth_config

    @abstractmethod
    async def store_payload(
        self,
        tokens: TokenDTOType,
        request: Request,
    ) -> None:
        """
        Get a payload from the tokens and store it to the request state.

        Parameters
        ----------
        tokens : TokenDTOType
            client's tokens

        request : Request
            request from the client
        """
        raise NotImplementedError

    @abstractmethod
    async def store_tokens(
        self,
        tokens: TokenDTOType,
        request: Request,
    ) -> None:
        """
        Store tokens to the request state.

        Parameters
        ----------
        tokens : TokenDTOType
            client's tokens

        request : Request
            request from the client
        """
        raise NotImplementedError

    @abstractmethod
    async def check_admin_rights(
        self,
        request: Request,
    ) -> None:
        """
        Check the admin rights.

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

    @abstractmethod
    async def validate_tokens(
        self,
        request: Request,
    ) -> TokenDTOType:
        """
        Validate a client's tokens.

        Parameters
        ----------
        request : Request
            request from the client

        Returns
        -------
        TokenDTOType
            received tokens

        Raises
        ------
        InvalidTokenError
            token does not exist
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_tokens(
        self,
        payload: PayloadType,
        request: Request,
    ) -> None:
        """
        Generate all tokens.

        Parameters
        ----------
        payload : PayloadType
            payload data

        request : Request
            request from the client
        """
        raise NotImplementedError

    @abstractmethod
    async def update_tokens(
        self,
        updated_payload: PayloadType,
        request: Request,
        response: Response,
    ) -> None:
        """
        Update all tokens.

        Parameters
        ----------
        updated_payload : PayloadType
            updated payload data

        request : Request
            request from the client

        response : Response
            response to the client
        """
        raise NotImplementedError

    @abstractmethod
    async def clear_tokens(
        self,
        request: Request,
        response: Response,
        user_id: TokenKeyType | None = None,
    ) -> None:
        """
        Clear all tokens.

        Parameters
        ----------
        request : Request
            request from the client

        response : Response
            response to the client

        user_id : TokenKeyType | None, optional
            user id, by default None
        """
        raise NotImplementedError

    @abstractmethod
    async def save_tokens(
        self,
        request: Request,
        response: Response,
    ) -> None:
        """
        Save tokens in cookie.

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
    ) -> PayloadType:
        """
        Get a payload data.

        Parameters
        ----------
        request : Request
            request from the client

        Returns
        -------
        BasePayload
            stored payload data
        """
        raise NotImplementedError
