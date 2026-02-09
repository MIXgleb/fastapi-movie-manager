__all__ = (
    "BaseMovieRepository",
    "BaseUserRepository",
    "MovieRepository",
    "UserRepository",
)

from app.database.repositories.movie import (
    BaseMovieRepository,
    MovieRepository,
)
from app.database.repositories.user import (
    BaseUserRepository,
    UserRepository,
)
