__all__ = (
    "AuthService",
    "BaseAuthService",
    "BaseMovieService",
    "BaseUserService",
    "MovieService",
    "UserService",
)

from abc import ABC, abstractmethod
from typing import Any, final, override

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.database import (
    BaseDatabaseHelper,
    BaseUOW,
    DbUOW,
    SqlAlchemyDatabaseHelper,
    SqlAlchemyUOW,
)
from app.services.auth import AuthService, BaseAuthService
from app.services.base import BaseDatabaseService, BaseService, BaseSqlAlchemyService
from app.services.movie import BaseMovieService, MovieService
from app.services.user import BaseUserService, UserService


class BaseServiceHelper[UOWType: BaseUOW](ABC):
    __slots__ = ("type_service",)

    type_uow: type[UOWType]

    @abstractmethod
    async def service_getter(self) -> BaseService:
        """Get an instance of the service.

        Returns
        -------
        BaseService
            service instance
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def service(self) -> BaseService:
        """Service.

        Returns
        -------
        BaseService
            service instance
        """
        raise NotImplementedError


class BaseDatabaseServiceHelper[
    Engine,
    Session,
    SessionFactory,
    Service: BaseDatabaseService[Any, Any, Any],
](
    BaseServiceHelper[
        DbUOW[
            Engine,
            Session,
            SessionFactory,
        ]
    ],
):
    __slots__ = ("db",)

    type_uow: type[DbUOW[Engine, Session, SessionFactory]]
    type_db: type[BaseDatabaseHelper[Engine, Session, SessionFactory]]

    def __init__(self, type_service: type[Service]) -> None:
        """Initialize the database service helper.

        Parameters
        ----------
        type_service : type[Service]
            type of service database
        """
        self.type_service = type_service
        self.db = self.type_db()

    @override
    async def service_getter(self) -> Service:
        return self.type_service(self.type_uow, self.db)

    @property
    @override
    def service(self) -> Service:
        return self.type_service(self.type_uow, self.db)


@final
class SqlAlchemyServiceHelper[Service: BaseSqlAlchemyService](
    BaseDatabaseServiceHelper[
        AsyncEngine,
        AsyncSession,
        async_sessionmaker[AsyncSession],
        Service,
    ]
):
    type_uow = SqlAlchemyUOW
    type_db = SqlAlchemyDatabaseHelper
