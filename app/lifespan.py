from collections.abc import (
    AsyncGenerator,
)
from contextlib import (
    asynccontextmanager,
)

from fastapi import (
    FastAPI,
)
from loguru import (
    logger,
)

from app.core import (
    settings,
)
from app.core.constants import (
    DISABLED_LOGGERS,
    EXTERNAL_LOGGERS,
)
from app.core.logging_ import (
    setup_logger,
)
from app.database.db_managers import (
    SqlAlchemyDatabaseManager,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """
    Initialize the fastapi application lifespan.

    Parameters
    ----------
    _ : FastAPI
        fastapi application instance
    """
    setup_logger(
        logging_config=settings.logging,
        external_loggers=EXTERNAL_LOGGERS,
        disabled_loggers=DISABLED_LOGGERS,
    )

    # ===========================================================================
    logger.info("🚀 Application starting up...")
    # ===========================================================================

    # ---------------------------------------------------------------------------
    # Database
    # ---------------------------------------------------------------------------
    logger.info("Connecting to database...")
    database_manager = SqlAlchemyDatabaseManager()
    await database_manager.init(
        url=settings.db.async_url,
        db_config=settings.db.sqla,
    )
    logger.info("Connection to database complete.")

    # ===========================================================================

    yield

    # ===========================================================================
    logger.info("🛑 Application shutting down...")
    # ===========================================================================

    # ---------------------------------------------------------------------------
    # Database
    # ---------------------------------------------------------------------------
    logger.info("Disconnecting from the database...")
    await database_manager.close()
    logger.info("Disconnection from the database complete.")
