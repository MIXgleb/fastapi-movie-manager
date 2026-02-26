from app.api.v1.schemas.base import (
    BaseResponse,
)


class ResponseRegisterNewUser(BaseResponse):
    """Response scheme for registering a new user."""

    message: str = "New user created."


class ResponseSuccessLogin(BaseResponse):
    """Response scheme for successful login."""

    message: str = "Logged in successfully."


class ResponseSuccessLogout(BaseResponse):
    """Response scheme for successful logout."""

    message: str = "Logged out successfully."
