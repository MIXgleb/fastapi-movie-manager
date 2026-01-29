import functools
from abc import ABC, abstractmethod
from typing import Any, final, override

from app.database import (
    BaseDatabaseHelper,
    BaseDatabaseUOW,
    BaseUOW,
)
from app.services.base import BaseDatabaseService, BaseService


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

    @functools.cached_property
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
        BaseDatabaseUOW[
            Engine,
            Session,
            SessionFactory,
        ],
    ],
):
    __slots__ = ("db",)

    type_uow: type[BaseDatabaseUOW[Engine, Session, SessionFactory]]
    type_db: type[BaseDatabaseHelper[Engine, Session, SessionFactory]]

    def __init__(
        self,
        type_service: type[Service],
    ) -> None:
        """Initialize the database service helper.

        Parameters
        ----------
        type_service : type[Service]
            type of service database
        """
        self.type_service = type_service
        self.db = self.type_db()

    @final
    @override
    async def service_getter(self) -> Service:
        return self.service

    @final
    @functools.cached_property
    @override
    def service(self) -> Service:
        return self.type_service(self.type_uow, self.db)
