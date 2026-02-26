from abc import (
    ABC,
    abstractmethod,
)
from types import (
    TracebackType,
)
from typing import (
    Self,
)

from pydantic import (
    BaseModel as BaseSchema,
)

from app.database.db_managers import (
    BaseDatabaseManager,
)
from app.database.repositories import (
    BaseMovieRepository,
    BaseUserRepository,
)


class BaseUOW(ABC):
    """Basic abstract unit-of-work class."""

    async def __aenter__(self) -> Self:
        """
        Enter to the asynchronous UOW manager.

        Returns
        -------
        Self
            self instance
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Exit the asynchronous UOW manager.

        Parameters
        ----------
        exc_type : type[BaseException] | None
            type of exception

        exc_val : BaseException | None
            value of exception

        exc_tb : TracebackType | None
            traceback
        """
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction in progress."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction in progress."""
        raise NotImplementedError


class BaseDatabaseUOW[
    EngineType,
    SessionType,
    SessionFactoryType,
    DatabaseConfigType: BaseSchema,
](BaseUOW):
    """Basic abstract database unit-of-work class."""

    users: BaseUserRepository[SessionType]
    movies: BaseMovieRepository[SessionType]

    @abstractmethod
    def __init__(
        self,
        database_manager: BaseDatabaseManager[
            EngineType,
            SessionType,
            SessionFactoryType,
            DatabaseConfigType,
        ],
    ) -> None:
        """
        Initialize the database unit-of-work.

        Parameters
        ----------
        database_manager : BaseDatabaseManager
            database manager
        """
        raise NotImplementedError
