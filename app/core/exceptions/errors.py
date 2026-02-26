from fastapi import (
    HTTPException,
    status,
)
from fastapi.exceptions import (
    RequestValidationError,
)

from app.core.typing_ import (
    DictRequestValidationError,
)


class ExpiredTokenError(HTTPException):
    """Expired token error."""

    def __init__(self) -> None:
        """
        Initialize the exception.

        status code: 401
        error message: Token was expired.
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token was expired.",
        )


class InvalidTokenError(HTTPException):
    """Invalid token error."""

    def __init__(
        self,
        detail: str = "Invalid token. Please try to log in again.",
    ) -> None:
        """
        Initialize the exception.

        status code: 401

        Parameters
        ----------
        detail : str, optional
            error message, by default "Invalid token. Please try to log in again."
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class AuthorizationError(HTTPException):
    """Authorization error."""

    def __init__(
        self,
        detail: str,
    ) -> None:
        """
        Initialize the exception.

        status code: 401

        Parameters
        ----------
        detail : str
            error message
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class UserExistsError(HTTPException):
    """User existence error."""

    def __init__(
        self,
        detail: str = "User already exists.",
    ) -> None:
        """
        Initialize the exception.

        status code: 409

        Parameters
        ----------
        detail : str, optional
            error message, by default "User already exists."
        """
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class ResourceNotFoundError(HTTPException):
    """Resource not found error."""

    def __init__(
        self,
        details: str,
    ) -> None:
        """
        Initialize the exception.

        status code: 404

        Parameters
        ----------
        details : str
            error message
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=details,
        )


class UserPermissionError(HTTPException):
    """User access permission error."""

    def __init__(self) -> None:
        """
        Initialize the exception.

        status code: 403
        error message: Insufficient access rights.
        """
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient access rights.",
        )


class ResourceOwnershipError(HTTPException):
    """Resource ownership error."""

    def __init__(self) -> None:
        """
        Initialize the exception.

        status code: 403
        error message: Resource ownership error.
        """
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource ownership error.",
        )


class IncorrectMethodError(HTTPException):
    """Incorrect method error."""

    def __init__(self) -> None:
        """
        Initialize the exception.

        status code: 405
        """
        super().__init__(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class QueryValueError(
    RequestValidationError,
    AttributeError,
):
    """Request query value error."""

    def __init__(
        self,
        query_value: str,
        query_key: str,
    ) -> None:
        """
        Initialize the exception.

        Parameters
        ----------
        query_value : str
            missing attribute

        query_key : str
            key to the missing attribute
        """
        super().__init__(
            errors=[
                DictRequestValidationError(
                    loc=["query", query_key],
                    msg=f"There is no {query_value!r} attribute",
                    type="incorrect_query_value",
                ),
            ]
        )


class DatabaseSessionError(OSError):
    """Database session error."""

    def __init__(self) -> None:
        """
        Initialize the exception.

        error message: Database session has not been initialized.
        """
        super().__init__("Database session has not been initialized.")


class ImmutableValueError(ValueError):
    """Immutable value error."""

    def __init__(
        self,
        field: str,
    ) -> None:
        """
        Initialize the exception.

        error message: Field {field} is immutable and cannot be modified.

        Parameters
        ----------
        field : str
            field name
        """
        super().__init__(f"Field {field!r} is immutable and cannot be modified.")
