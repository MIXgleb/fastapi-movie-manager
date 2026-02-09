from typing import (
    final,
)

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.database import (
    SqlAlchemyDatabaseHelper,
    SqlAlchemyUOW,
)
from app.services.base import (
    BaseSqlAlchemyService,
)
from app.services.service_helpers.base import (
    BaseDatabaseServiceHelper,
)


@final
class SqlAlchemyServiceHelper[Service: BaseSqlAlchemyService](
    BaseDatabaseServiceHelper[
        AsyncEngine,
        AsyncSession,
        async_sessionmaker[AsyncSession],
        Service,
    ],
):
    type_uow = SqlAlchemyUOW
    type_db = SqlAlchemyDatabaseHelper
