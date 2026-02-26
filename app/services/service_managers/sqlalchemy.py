from typing import (
    final,
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
    SqlAlchemyDatabaseManager,
)
from app.database.unit_of_works import (
    SqlAlchemyUOW,
)
from app.services.base import (
    BaseSqlAlchemyService,
)
from app.services.service_managers.base import (
    BaseDatabaseServiceManager,
)


@final
class SqlAlchemyServiceManager[
    ServiceType: BaseSqlAlchemyService,
](
    BaseDatabaseServiceManager[
        AsyncEngine,
        AsyncSession,
        async_sessionmaker[AsyncSession],
        SqlAlchemyConfig,
        ServiceType,
    ],
):
    """SqlAlchemy service manager."""

    uow_class = SqlAlchemyUOW
    database_manager_class = SqlAlchemyDatabaseManager
