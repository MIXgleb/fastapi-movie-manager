from typing import (
    override,
)

from pydantic import (
    BaseModel as BaseSchema,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.core.config import (
    SqlAlchemyConfig,
)
from app.database.db_managers import (
    BaseDatabaseManager,
)
from app.database.unit_of_works import (
    BaseDatabaseUOW,
    BaseUOW,
)


class BaseService:
    """Basic abstract service class."""

    __slots__ = ("uow",)

    def __init__(
        self,
        uow_class: type[BaseUOW],
    ) -> None:
        """
        Initialize the service.

        Parameters
        ----------
        uow_class : type[BaseUOW]
            unit-of-work class
        """
        self.uow = uow_class()


class BaseDatabaseService[
    EngineType,
    SessionType,
    SessionFactoryType,
    DatabaseConfigType: BaseSchema,
](BaseService):
    """Basic abstract database service class."""

    @override
    def __init__(
        self,
        uow_class: type[
            BaseDatabaseUOW[
                EngineType,
                SessionType,
                SessionFactoryType,
                DatabaseConfigType,
            ]
        ],
        database_manager: BaseDatabaseManager[
            EngineType,
            SessionType,
            SessionFactoryType,
            DatabaseConfigType,
        ],
    ) -> None:
        """
        Initialize the database service.

        Parameters
        ----------
        uow_class : type[BaseDatabaseUOW]
            database unit-of-work class

        database_manager : BaseDatabaseManager
            database manager
        """
        self.uow = uow_class(database_manager)


class BaseSqlAlchemyService(
    BaseDatabaseService[
        AsyncEngine,
        AsyncSession,
        async_sessionmaker[AsyncSession],
        SqlAlchemyConfig,
    ],
):
    """Basic abstract sqlalchemy service class."""
