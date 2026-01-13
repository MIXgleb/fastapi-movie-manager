from types import TracebackType
from typing import Self, final, override

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

import app.core.exceptions as exc
from app.database.repositories import MovieRepository, UserRepository
from app.database.unit_of_works.base import BaseDatabaseUOW


@final
class SqlAlchemyUOW(
    BaseDatabaseUOW[
        AsyncEngine,
        AsyncSession,
        async_sessionmaker[AsyncSession],
    ],
):
    @override
    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        SqlAlchemyUOW.users = UserRepository(self._session)
        SqlAlchemyUOW.movies = MovieRepository(self._session)
        return await super().__aenter__()

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the asynchronous UOW manager.

        Parameters
        ----------
        exc_type : type[BaseException] | None
            type of exception

        exc_val : BaseException | None
            value of exception

        exc_tb : TracebackType | None
            traceback

        Raises
        ------
        DatabaseSessionError
            session is not initialized
        """
        if self._session is None:
            raise exc.DatabaseSessionError

        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self._session.close()
        self._session = None

    @override
    async def commit(self) -> None:
        """Commit the current transaction in progress.

        Raises
        ------
        DatabaseSessionError
            session is not initialized
        """
        if self._session is None:
            raise exc.DatabaseSessionError

        await self._session.commit()

    @override
    async def rollback(self) -> None:
        """Rollback the current transaction in progress.

        Raises
        ------
        DatabaseSessionError
            session is not initialized
        """
        if self._session is None:
            raise exc.DatabaseSessionError

        await self._session.rollback()
