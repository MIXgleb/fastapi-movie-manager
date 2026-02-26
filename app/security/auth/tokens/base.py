from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    final,
)

import jwt
from fastapi import (
    Response,
)
from pydantic import (
    BaseModel as BaseSchema,
)

import app.core.exceptions as exc
from app.core.config import (
    AuthTokenConfig,
)
from app.core.typing_ import (
    DictAnyAnyType,
)
from app.security.auth.schemas import (
    BasePayload,
)

type JWTokenType = str


class BaseAuthToken[
    TokenType,
    TokenConfigType: BaseSchema,
]:
    """Basic abstract auth token class."""

    __slots__ = ("_token", "token_config")

    def __init__(
        self,
        token_config: TokenConfigType,
        token: TokenType | None = None,
    ) -> None:
        """
        Initialize the token service.

        Parameters
        ----------
        token_config : TokenConfigType
            token config

        token : TokenType | None, optional
            current token, by default None
        """
        self._token = token
        self.token_config = token_config

    @property
    def token(self) -> TokenType:
        """
        Check and get a token.

        Returns
        -------
        TokenType
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
    def token(
        self,
        new_value: TokenType,
    ) -> None:
        self._token = new_value

    @token.deleter
    def token(self) -> None:
        self._token = None


class BaseSyncAuthToken[
    TokenType,
    TokenKeyType,
    PayloadType: BasePayload,
    TokenConfigType: BaseSchema,
](
    ABC,
    BaseAuthToken[
        TokenType,
        TokenConfigType,
    ],
):
    """Basic abstract auth synchronous token class."""

    @abstractmethod
    def create(
        self,
        payload: PayloadType,
    ) -> TokenType:
        """
        Create a token.

        Parameters
        ----------
        payload : PayloadType
            payload data

        Returns
        -------
        TokenType
            created token
        """
        raise NotImplementedError

    @abstractmethod
    def read(self) -> PayloadType:
        """
        Read a token.

        Returns
        -------
        PayloadType
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        response: Response,
        payload: PayloadType,
    ) -> None:
        """
        Update a token.

        Parameters
        ----------
        response : Response
            response to the client

        payload : PayloadType
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        response: Response,
    ) -> None:
        """
        Delete a token.

        Parameters
        ----------
        response : Response
            response to the client
        """
        raise NotImplementedError

    @abstractmethod
    def delete_by_key(
        self,
        key: TokenKeyType,
    ) -> None:
        """
        Delete a token by key.

        Parameters
        ----------
        key : TokenKeyType
            unique key
        """
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        response: Response,
        payload: PayloadType | None,
    ) -> None:
        """
        Save a token.

        Parameters
        ----------
        response : Response
            response to the client

        payload : PayloadType | None
            payload data
        """
        raise NotImplementedError


class BaseAsyncAuthToken[
    TokenType,
    TokenKeyType,
    PayloadType: BasePayload,
    TokenConfigType: BaseSchema,
](
    ABC,
    BaseAuthToken[
        TokenType,
        TokenConfigType,
    ],
):
    """Basic abstract auth asynchronous token class."""

    @abstractmethod
    async def create(
        self,
        payload: PayloadType,
    ) -> TokenType:
        """
        Create a token.

        Parameters
        ----------
        payload : PayloadType
            payload data

        Returns
        -------
        TokenType
            created token
        """
        raise NotImplementedError

    @abstractmethod
    async def read(self) -> PayloadType:
        """
        Read a token.

        Returns
        -------
        PayloadType
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        response: Response,
        payload: PayloadType,
    ) -> None:
        """
        Update a token.

        Parameters
        ----------
        response : Response
            response to the client

        payload : PayloadType
            payload data
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        response: Response,
    ) -> None:
        """
        Delete a token.

        Parameters
        ----------
        response : Response
            response to the client
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_by_key(
        self,
        key: TokenKeyType,
    ) -> None:
        """
        Delete a token by key.

        Parameters
        ----------
        key : TokenKeyType
            unique key
        """
        raise NotImplementedError

    @abstractmethod
    async def save(
        self,
        response: Response,
        payload: PayloadType | None,
    ) -> None:
        """
        Save a token.

        Parameters
        ----------
        response : Response
            response to the client

        payload : PayloadType | None
            payload data
        """
        raise NotImplementedError


class BaseAuthJWT[TokenType](
    BaseAuthToken[
        TokenType,
        AuthTokenConfig,
    ],
):
    """Basic auth abstract jwt class."""

    @final
    def _encrypt_jwtoken(
        self,
        dict_payload: DictAnyAnyType,
    ) -> JWTokenType:
        return jwt.encode(
            payload=dict_payload,
            key=self.token_config.secret_jwt_key.get_secret_value(),
            algorithm=self.token_config.algorithm.get_secret_value(),
        )

    @final
    def _decrypt_jwtoken(
        self,
        jwtoken: JWTokenType,
    ) -> DictAnyAnyType:
        return jwt.decode(
            jwt=jwtoken,
            key=self.token_config.secret_jwt_key.get_secret_value(),
            algorithms=[
                self.token_config.algorithm.get_secret_value(),
            ],
        )
