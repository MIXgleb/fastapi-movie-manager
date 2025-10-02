from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from app.api import router as api_router
from app.core.config import settings
from app.core.exceptions import (
    database_exception_handler,
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.loggers import setup_logger
from app.core.middlewares import CORSMiddleware, LoggingMiddleware
from app.database import SqlAlchemyDbHelper


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """Initialize the fastapi application lifespan.

    Parameters
    ----------
    _ : FastAPI
        fastapi application instance

    Returns
    -------
    AsyncGenerator[None]
        open before launching, close before completion
    """  # noqa: DOC202
    setup_logger()
    logger.info("🚀 Application starting up...")

    logger.info("Connecting to redis...")
    redis_connection = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db_request_limiter,
        encoding=settings.redis.encoding,
    )
    await redis_connection.ping()  # type: ignore[reportUnknownMemberType]
    logger.info("Connection to redis completed.")

    logger.info("Connecting to database...")
    db = SqlAlchemyDbHelper()
    await db.init(str(settings.db.url))
    logger.info("Connection to database completed.")

    await FastAPILimiter.init(redis_connection)  # type: ignore[reportUnknownMemberType]

    yield

    await FastAPILimiter.close()

    logger.info("🛑 Application shutting down...")
    logger.info("Disconnecting from the database...")
    await db.close()


app = FastAPI(
    title="Movie manager",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    swagger_ui_oauth2_redirect_url=None,
)

app.include_router(api_router)

app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
