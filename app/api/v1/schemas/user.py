from datetime import datetime
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from app.domains import UserRoleType

USER_USERNAME_PATTERN: Final[str] = r"^[\w\d_\-]+$"
USERNAME_INPUT_FIELD: Final = Field(max_length=20, pattern=USER_USERNAME_PATTERN)
PASSWORD_INPUT_FIELD: Final = Field(min_length=5, max_length=30)


class UserBase(BaseModel):
    username: str = USERNAME_INPUT_FIELD


class UserPasswordBase(BaseModel):
    password: str = PASSWORD_INPUT_FIELD


class UserHashedPasswordBase(BaseModel):
    hashed_password: str


class UserInputDTO(UserBase, UserPasswordBase): ...


class UserCreateDTO(UserBase, UserHashedPasswordBase):
    role: UserRoleType


class UserUpdateDTO(UserPasswordBase): ...


class UserUpdateWithHashedPasswordDTO(UserHashedPasswordBase): ...


class UserOutputDTO(UserBase):
    id: int
    role: UserRoleType
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserFilterDTO(BaseModel):
    limit: int = Field(default=10, le=100, ge=1)
    offset: int = Field(default=0, ge=0)
    sort_by: str = Field(default="id", validation_alias="sort-by")
    username_contains: str | None = Field(default=None, validation_alias="username-contains")
    role: list[UserRoleType] | None = None

    model_config = ConfigDict(populate_by_name=True)


class UpdateUserResponse(BaseModel):
    message: str = "User has been updated successfully."


class DeleteUserResponse(BaseModel):
    message: str = "User has been removed successfully."
    user: UserOutputDTO
