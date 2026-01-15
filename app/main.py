from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException
from starlette.middleware.exceptions import ExceptionMiddleware

from app.api import router as api_router
from app.core import settings
from app.core.exceptions import (
    database_exception_handler,
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.logging import setup_logger
from app.core.middlewares import (
    AuthMiddleware,
    CORSMiddleware,
    LoggingMiddleware,
)
from app.database import SqlAlchemyDatabaseHelper


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """Initialize the fastapi application lifespan.

    Parameters
    ----------
    _ : FastAPI
        fastapi application instance

    Returns
    -------
    AsyncGenerator
        open before launching, close before completion
    """  # noqa: DOC202
    logger.info("🚀 Application starting up...")

    setup_logger()

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
    db = SqlAlchemyDatabaseHelper()
    await db.init(str(settings.db.url))
    logger.info("Connection to database completed.")

    await FastAPILimiter.init(redis_connection)  # type: ignore[reportUnknownMemberType]

    yield

    await FastAPILimiter.close()

    logger.info("🛑 Application shutting down...")
    logger.info("Disconnecting from the database...")
    await db.close()


# FastAPI app
app = FastAPI(
    title="Movie manager",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    swagger_ui_oauth2_redirect_url=None,
)

# Routers
app.include_router(api_router)

# Exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Middlewares
app.add_middleware(
    AuthMiddleware,
    only_admin_urls=(
        "/api/docs",
        "/api/docs/oauth2-redirect",
        "/api/redoc",
        "/api/openapi.json",
    ),
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware)
app.add_middleware(
    ExceptionMiddleware,
    handlers=app.exception_handlers,
)
