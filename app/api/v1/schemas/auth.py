from pydantic import (
    BaseModel,
)


class RegisterResponse(BaseModel):
    message: str = "New user created."


class LoginResponse(BaseModel):
    message: str = "Logged in successfully."


class LogoutResponse(BaseModel):
    message: str = "Logged out successfully."
