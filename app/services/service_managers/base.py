from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    final,
    override,
)

from pydantic import (
    BaseModel as BaseSchema,
)

from app.core.typing_ import (
    KwargsType,
)
from app.database.db_managers import (
    BaseDatabaseManager,
)
from app.database.unit_of_works import (
    BaseDatabaseUOW,
    BaseUOW,
)
from app.services.base import (
    BaseDatabaseService,
    BaseService,
)


class BaseServiceManager[
    UOWType: BaseUOW,
    ServiceType: BaseService,
](ABC):
    """Basic abstract service manager class."""

    __slots__ = ("service_class", "service_kwargs")

    uow_class: type[UOWType]

    def __init__(
        self,
        service_class: type[ServiceType],
        **service_kwargs: KwargsType,
    ) -> None:
        """
        Initialize the service manager.

        Parameters
        ----------
        service_class : type[ServiceType]
            service class

        **service_kwargs : KwargsType
            keyword arguments for service constructor
        """
        self.service_class = service_class
        self.service_kwargs = service_kwargs

    @abstractmethod
    async def service_getter(self) -> ServiceType:
        """
        Get an instance of the service.

        Returns
        -------
        ServiceType
            service instance
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def service(self) -> ServiceType:
        """
        Get service.

        Returns
        -------
        ServiceType
            service instance
        """
        raise NotImplementedError


class BaseDatabaseServiceManager[
    EngineType,
    SessionType,
    SessionFactoryType,
    DatabaseConfigType: BaseSchema,
    ServiceType: BaseDatabaseService[Any, Any, Any, Any],
](
    BaseServiceManager[
        BaseDatabaseUOW[
            EngineType,
            SessionType,
            SessionFactoryType,
            DatabaseConfigType,
        ],
        ServiceType,
    ],
):
    """Basic abstract database service manager class."""

    __slots__ = ("database_manager",)

    uow_class: type[
        BaseDatabaseUOW[
            EngineType,
            SessionType,
            SessionFactoryType,
            DatabaseConfigType,
        ]
    ]
    database_manager_class: type[
        BaseDatabaseManager[
            EngineType,
            SessionType,
            SessionFactoryType,
            DatabaseConfigType,
        ]
    ]

    @override
    def __init__(
        self,
        service_class: type[ServiceType],
        **service_kwargs: KwargsType,
    ) -> None:
        super().__init__(
            service_class=service_class,
            **service_kwargs,
        )
        self.database_manager = self.database_manager_class()

    @final
    @override
    async def service_getter(self) -> ServiceType:
        return self.service

    @final
    @property
    @override
    def service(self) -> ServiceType:
        return self.service_class(
            self.uow_class,
            self.database_manager,
            **self.service_kwargs,
        )
