from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from typing import (
    ClassVar,
    Literal,
    final,
)

type TypeUserRole = Literal["guest", "user", "admin"]


@final
class UserRole:
    guest: ClassVar[TypeUserRole] = "guest"
    user: ClassVar[TypeUserRole] = "user"
    admin: ClassVar[TypeUserRole] = "admin"


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
    role: list[TypeUserRole] | None
