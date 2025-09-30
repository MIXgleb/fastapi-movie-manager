__all__ = (
    "MovieDM",
    "MovieFilterDM",
    "UserDM",
    "UserFilterDM",
    "UserRole",
    "UserRoleType",
)

from typing import ClassVar, Protocol

from app.domains.movie import MovieDM, MovieFilterDM
from app.domains.user import (
    UserDM,
    UserFilterDM,
    UserRole,
    UserRoleType,
)


class DataclassType(Protocol):
    __dataclass_fields__: ClassVar
