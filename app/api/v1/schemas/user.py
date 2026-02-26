from datetime import (
    datetime,
)

from pydantic import (
    BaseModel as BaseSchema,
)
from pydantic.config import (
    ConfigDict,
)
from pydantic.fields import (
    Field,
)

from app.api.v1.schemas.base import (
    BaseResponse,
)
from app.core.constants import (
    USER_PASSWORD_FIELD,
    USER_USERNAME_FIELD,
)
from app.domains import (
    UserRole,
)


class BaseUserUsernameDTO(BaseSchema):
    """Basic scheme of a user's username."""

    username: str = USER_USERNAME_FIELD


class BaseUserPasswordDTO(BaseSchema):
    """Basic scheme of a user's password."""

    password: str = USER_PASSWORD_FIELD


class BaseUserHashedPasswordDTO(BaseSchema):
    """Basic scheme of a user's hashed password."""

    hashed_password: str


class UserInputDTO(
    BaseUserUsernameDTO,
    BaseUserPasswordDTO,
):
    """Scheme of getting a user."""


class UserCreateDTO(
    BaseUserUsernameDTO,
    BaseUserHashedPasswordDTO,
):
    """Scheme of creating a user."""

    role: UserRole


class UserUpdateDTO(BaseUserPasswordDTO):
    """Scheme of updating a user."""


class UserHashedUpdateDTO(BaseUserHashedPasswordDTO):
    """Scheme of updating a hashed user."""


class UserOutputDTO(BaseUserUsernameDTO):
    """Scheme of returning a user."""

    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserFilterDTO(BaseSchema):
    """Scheme of filtering a user."""

    limit: int = Field(default=10, le=100, ge=1)
    offset: int = Field(default=0, ge=0)
    sort_by: str = Field(default="id", validation_alias="sort-by")
    username_contains: str | None = Field(default=None, validation_alias="username-contains")
    role: list[UserRole] | None = None

    model_config = ConfigDict(populate_by_name=True)


class ResponseUpdateUser(BaseResponse):
    """Response scheme for updating a user."""

    message: str = "User has been updated successfully."


class ResponseDeleteUser(BaseResponse):
    """Response scheme for deleting a user."""

    message: str = "User has been removed successfully."
    user: UserOutputDTO
