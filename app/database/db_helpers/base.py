from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import ClassVar, Self, final

import app.core.exceptions as exc


class BaseDatabaseHelper[
    Engine,
    Session,
    SessionFactory,
](ABC):
    __slots__ = ("_engine", "_session_factory")

    _instance: ClassVar[Self | None] = None

    @final
    def __new__(cls) -> Self:
        """Singleton.

        Returns
        -------
        Self
            only instance of the class
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the database helper."""
        self._engine: Engine | None = None
        self._session_factory: SessionFactory | None = None

    @abstractmethod
    async def init(
        self,
        url: str,
    ) -> None:
        """Initialize the db session.

        Parameters
        ----------
        url : str
            connection url
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """Close the db session."""
        raise NotImplementedError

    @abstractmethod
    async def session_getter(self) -> AsyncGenerator[Session]:
        """Get the created db session.

        Yields
        ------
        AsyncGenerator[Session]
            instance of db session
        """
        raise NotImplementedError
        yield

    @final
    @property
    def session_factory(self) -> SessionFactory:
        """Get the session factory.

        Returns
        -------
        SessionFactory
            session factory

        Raises
        ------
        DatabaseSessionError
            session is not initialized
        """
        if self._session_factory is None:
            raise exc.DatabaseSessionError

        return self._session_factory
