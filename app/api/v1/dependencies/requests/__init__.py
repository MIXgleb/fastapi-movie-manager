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
)


from app.api.v1.dependencies.requests.auth import (
    AuthLoginDep,
    AuthLogoutDep,
    AuthRegisterDep,
)
from app.api.v1.dependencies.requests.movie import (
    MovieCreateDep,
    MovieDeleteDep,
    MovieGetAllDep,
    MovieGetDep,
    MovieOwnershipDep,
    MovieUpdateDep,
)
from app.api.v1.dependencies.requests.user import (
    UserDeleteDep,
    UserDeleteMeDep,
    UserGetAllDep,
    UserGetDep,
    UserGetMeDep,
    UserOwnershipDep,
    UserUpdateDep,
    UserUpdateMeDep,
)
