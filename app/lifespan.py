from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from loguru import logger

from app.core import settings
from app.core.logging import setup_logger
from app.database import SqlAlchemyDatabaseHelper


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """Initialize the fastapi application lifespan.

    Parameters
    ----------
    _ : FastAPI
        fastapi application instance
    """
    setup_logger()

    # ===========================================================================
    logger.info("🚀 Application starting up...")
    # ===========================================================================
    # ---------------------------------------------------------------------------
    # Redis
    # ---------------------------------------------------------------------------
    logger.info("Connecting to redis...")
    redis_connection = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db_request_limiter,
        encoding=settings.redis.encoding,
    )
    await redis_connection.ping()
    logger.info("Connection to redis complete.")

    # ---------------------------------------------------------------------------
    # Database
    # ---------------------------------------------------------------------------
    logger.info("Connecting to database...")
    db = SqlAlchemyDatabaseHelper()
    await db.init(str(settings.db.url))
    logger.info("Connection to database complete.")

    # ---------------------------------------------------------------------------
    # FastAPI Limiter
    # ---------------------------------------------------------------------------
    logger.info("Initializing the FastAPI Limiter...")
    await FastAPILimiter.init(redis_connection)
    logger.info("FastAPI Limiter initialization complete.")
    # ===========================================================================

    yield

    # ===========================================================================
    logger.info("🛑 Application shutting down...")
    # ===========================================================================
    # ---------------------------------------------------------------------------
    # FastAPI Limiter
    # ---------------------------------------------------------------------------
    logger.info("Closing the FastAPI limiter...")
    await FastAPILimiter.close()
    logger.info("FastAPI limiter closure complete.")

    # ---------------------------------------------------------------------------
    # Database
    # ---------------------------------------------------------------------------
    logger.info("Disconnecting from the database...")
    await db.close()
    logger.info("Disconnection from the database complete.")
