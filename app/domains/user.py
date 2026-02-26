from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from enum import (
    StrEnum,
)

from app.domains.base import (
    BaseDataclass,
)


class UserRole(StrEnum):
    """User roles."""

    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"


@dataclass(slots=True, frozen=True)
class UserInputDM(BaseDataclass):
    """Domain model of getting a user."""

    username: str
    password: str


@dataclass(slots=True, frozen=True)
class UserCreateDM(BaseDataclass):
    """Domain model of creating a user."""

    username: str
    hashed_password: str
    role: UserRole


@dataclass(slots=True, frozen=True)
class UserUpdateDM(BaseDataclass):
    """Domain model of updating a user."""

    password: str | None


@dataclass(slots=True, frozen=True)
class UserHashedUpdateDM(UserUpdateDM):
    """Domain model of updating a hashed user."""

    hashed_password: str | None


@dataclass(slots=True, frozen=True)
class UserOutputDM(BaseDataclass):
    """Domain model of returning a user."""

    username: str
    role: UserRole
    created_at: datetime


@dataclass(slots=True, frozen=True)
class UserFiltersDM(BaseDataclass):
    """Domain model of filtering a user."""

    limit: int
    offset: int
    sort_by: str
    username_contains: str | None
    role: list[UserRole] | None
