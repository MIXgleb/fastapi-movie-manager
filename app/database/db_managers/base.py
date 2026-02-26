from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    ClassVar,
    Self,
    final,
)

from pydantic import (
    BaseModel as BaseSchema,
)

import app.core.exceptions as exc


class BaseDatabaseManager[
    EngineType,
    SessionType,
    SessionFactoryType,
    DatabaseConfigType: BaseSchema,
](ABC):
    """Basic abstract database manager class."""

    __slots__ = ("_engine", "_session_factory")

    _instance: ClassVar[Self | None] = None

    @final
    def __new__(cls) -> Self:
        """
        Singleton.

        Returns
        -------
        Self
            only instance of the class
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the database manager."""
        self._engine: EngineType | None = None
        self._session_factory: SessionFactoryType | None = None

    @abstractmethod
    async def init(
        self,
        url: str,
        db_config: DatabaseConfigType,
    ) -> None:
        """
        Initialize a db session.

        Parameters
        ----------
        url : str
            connection url

        db_config : DatabaseConfigType
            database config
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """Close a db session."""
        raise NotImplementedError

    @final
    @property
    def session_factory(self) -> SessionFactoryType:
        """
        Get the session factory.

        Returns
        -------
        SessionFactoryType
            session factory

        Raises
        ------
        DatabaseSessionError
            session is not initialized
        """
        if self._session_factory is None:
            raise exc.DatabaseSessionError

        return self._session_factory
