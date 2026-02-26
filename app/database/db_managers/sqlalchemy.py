from typing import (
    final,
    override,
)

from sqlalchemy.engine import (
    URL,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import (
    SqlAlchemyConfig,
)
from app.database.db_managers.base import (
    BaseDatabaseManager,
)


@final
class SqlAlchemyDatabaseManager(
    BaseDatabaseManager[
        AsyncEngine,
        AsyncSession,
        async_sessionmaker[AsyncSession],
        SqlAlchemyConfig,
    ],
):
    """SqlAlchemy database manager."""

    @override
    async def init(
        self,
        url: str | URL,
        db_config: SqlAlchemyConfig,
    ) -> None:
        self._engine = create_async_engine(
            url=url,
            echo=db_config.echo,
            echo_pool=db_config.echo_pool,
            pool_size=db_config.pool_size,
            max_overflow=db_config.max_overflow,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @override
    async def close(self) -> None:
        if self._engine is None:
            return

        await self._engine.dispose()
        self._engine = None
        self._session_factory = None
