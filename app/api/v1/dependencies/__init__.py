__all__ = (
    "UserOwnership",
    "dep_movie_ownership_getter",
    "dep_permission_getter",
)

from app.api.v1.dependencies.ownerships import (
    UserOwnership,
    dep_movie_ownership_getter,
)
from app.api.v1.dependencies.rbac import (
    dep_permission_getter,
)
