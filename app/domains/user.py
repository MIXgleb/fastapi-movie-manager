from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, Literal, final

type UserRoleType = Literal["guest", "user", "admin"]


@final
class UserRole:
    guest: ClassVar[UserRoleType] = "guest"
    user: ClassVar[UserRoleType] = "user"
    admin: ClassVar[UserRoleType] = "admin"


@dataclass(slots=True)
class UserDM:
    id: int
    username: str
    hashed_password: str
    role: str
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class UserFilterDM:
    limit: int
    offset: int
    sort_by: str
    username_contains: str | None
    role: list[UserRoleType] | None
