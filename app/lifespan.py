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
from app.core.logging import (
    setup_logger,
)
from app.database import (
    SqlAlchemyDatabaseHelper,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """Initialize the fastapi application lifespan.

    Parameters
    ----------
    _ : FastAPI
        fastapi application instance
    """
    setup_logger(
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
    db = SqlAlchemyDatabaseHelper()
    await db.init(str(settings.db.url))
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
    await db.close()
    logger.info("Disconnection from the database complete.")
