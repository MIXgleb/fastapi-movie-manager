__all__ = (
    "MovieDM",
    "MovieFilterDM",
    "TypeUserRole",
    "UserDM",
    "UserFilterDM",
    "UserRole",
)

from typing import ClassVar, Protocol

from app.domains.movie import MovieDM, MovieFilterDM
from app.domains.user import (
    TypeUserRole,
    UserDM,
    UserFilterDM,
    UserRole,
)


class DataclassType(Protocol):
    __dataclass_fields__: ClassVar
