from abc import ABC, abstractmethod
from types import TracebackType
from typing import ClassVar, Self

from app.database.db_helpers import BaseDatabaseHelper
from app.database.repositories import BaseMovieRepository, BaseUserRepository


class BaseUOW(ABC):
    async def __aenter__(self) -> Self:
        """Enter to the asynchronous UOW manager.

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
        """Exit the asynchronous UOW manager.

        Parameters
        ----------
        exc_type : type[BaseException] | None
            type of exception

        exc_val : BaseException | None
            value of exception

        exc_tb : TracebackType | None
            traceback
        """
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction in progress."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction in progress."""
        raise NotImplementedError


class BaseDatabaseUOW[
    Engine,
    Session,
    SessionFactory,
](BaseUOW):
    __slots__ = ("_session", "_session_factory")

    users: ClassVar[BaseUserRepository]
    movies: ClassVar[BaseMovieRepository]

    def __init__(
        self,
        db: BaseDatabaseHelper[
            Engine,
            Session,
            SessionFactory,
        ],
    ) -> None:
        """Initialize the database unit-of-work interface.

        Parameters
        ----------
        db : BaseDatabaseHelper
            database helper instance
        """
        self._session: Session | None = None
        self._session_factory = db.session_factory
