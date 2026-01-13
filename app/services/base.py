from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.database import BaseDatabaseHelper, BaseDatabaseUOW, BaseUOW


class BaseService:
    __slots__ = ("uow",)

    def __init__(
        self,
        type_uow: type[BaseUOW],
    ) -> None:
        """Initialize the service.

        Parameters
        ----------
        type_uow : type[BaseUOW]
            unit-of-work interface
        """
        self.uow = type_uow()


class BaseDatabaseService[
    Engine,
    Session,
    SessionFactory,
](BaseService):
    def __init__(
        self,
        type_uow: type[
            BaseDatabaseUOW[
                Engine,
                Session,
                SessionFactory,
            ]
        ],
        db: BaseDatabaseHelper[
            Engine,
            Session,
            SessionFactory,
        ],
    ) -> None:
        """Initialize the database service.

        Parameters
        ----------
        type_uow : type[BaseDatabaseUOW]
            database unit-of-work interface

        db : BaseDatabaseHelper
            database helper instance
        """
        self.uow = type_uow(db)


class BaseSqlAlchemyService(
    BaseDatabaseService[
        AsyncEngine,
        AsyncSession,
        async_sessionmaker[AsyncSession],
    ],
): ...
