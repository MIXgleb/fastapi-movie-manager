from collections.abc import (
    AsyncGenerator,
)
from typing import (
    final,
    override,
)

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import app.core.exceptions as exc
from app.core import (
    settings,
)
from app.database.db_helpers.base import (
    BaseDatabaseHelper,
)


@final
class SqlAlchemyDatabaseHelper(
    BaseDatabaseHelper[
        AsyncEngine,
        AsyncSession,
        async_sessionmaker[AsyncSession],
    ],
):
    @override
    async def init(
        self,
        url: str,
    ) -> None:
        self._engine = create_async_engine(
            url=url,
            echo=settings.db.echo,
            echo_pool=settings.db.echo_pool,
            pool_size=settings.db.pool_size,
            max_overflow=settings.db.max_overflow,
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

    @override
    async def session_getter(self) -> AsyncGenerator[AsyncSession]:
        """Get the created db session.

        Yields
        ------
        AsyncGenerator[AsyncSession]
            instance of db session

        Raises
        ------
        DatabaseSessionError
            session is not initialized
        """
        if self._session_factory is None:
            raise exc.DatabaseSessionError

        async with self._session_factory() as session:
            yield session
