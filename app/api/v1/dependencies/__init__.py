__all__ = (
    "AuthLoginDep",
    "AuthLogoutDep",
    "AuthRegisterDep",
    "MovieCreateDep",
    "MovieDeleteDep",
    "MovieGetAllDep",
    "MovieGetAllDep",
    "MovieGetDep",
    "MovieOwnershipDep",
    "MovieUpdateDep",
    "UserDeleteDep",
    "UserDeleteMeDep",
    "UserGetAllDep",
    "UserGetDep",
    "UserGetMeDep",
    "UserOwnershipDep",
    "UserUpdateDep",
    "UserUpdateMeDep",
    "dep_movie_ownership_getter",
    "dep_permission_getter",
    "dep_user_ownership_getter",
)

from app.api.v1.dependencies.requests import (
    AuthLoginDep,
    AuthLogoutDep,
    AuthRegisterDep,
    MovieCreateDep,
    MovieDeleteDep,
    MovieGetAllDep,
    MovieGetDep,
    MovieOwnershipDep,
    MovieUpdateDep,
    UserDeleteDep,
    UserDeleteMeDep,
    UserGetAllDep,
    UserGetDep,
    UserGetMeDep,
    UserOwnershipDep,
    UserUpdateDep,
    UserUpdateMeDep,
)
from app.api.v1.dependencies.security.movie_ownership import (
    dep_movie_ownership_getter,
)
from app.api.v1.dependencies.security.rbac import (
    dep_permission_getter,
)
from app.api.v1.dependencies.security.user_ownership import (
    dep_user_ownership_getter,
)
