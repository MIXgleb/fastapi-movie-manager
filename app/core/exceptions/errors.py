from collections.abc import Sequence
from typing import Any, TypedDict

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


class CustomValidationErrorSchema(BaseModel):
    field: Sequence[Any]
    message: str
    extra_message: dict[Any, Any]
    type: str


class TokenExpiredError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token was expired.",
        )


class InvalidTokenError(HTTPException):
    def __init__(
        self,
        detail: str = "Invalid token. Please try to log in again.",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class AuthorizationError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class UserExistsError(HTTPException, FileExistsError):
    def __init__(
        self,
        detail: str = "User already exists.",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class ResourceNotFoundError(HTTPException, FileNotFoundError):
    def __init__(self, details: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=details,
        )


class UserPermissionError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient access rights.",
        )


class ResourceOwnershipError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource ownership error.",
        )


class WrondMethodError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class QueryValueError(RequestValidationError, AttributeError):
    def __init__(self, query_value: str, query_key: str) -> None:
        super().__init__([
            QueryValueError._DictRequestValidationError(
                loc=["query", query_key],
                msg=f"There is no {query_value!r} attribute",
                type="wrong_query_value",
            )
        ])

    class _DictRequestValidationError(TypedDict):
        """Typed dict."""

        loc: Sequence[str]
        msg: str
        type: str


class DatabaseSessionError(OSError):
    def __init__(self) -> None:
        super().__init__("Database session has not been initialized.")
