from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

from app.api import api_v1_router, common_router
from app.core import settings
from app.core.exceptions import (
    database_exception_handler,
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.middlewares import (
    AuthMiddleware,
    CORSMiddleware,
    ExceptionMiddleware,
    LoggingMiddleware,
)
from app.core.typing import ExcludedLogRequest
from app.lifespan import lifespan

# FastAPI application
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
app.include_router(common_router)
app.include_router(
    router=api_v1_router,
    prefix=settings.api.prefix,
)


# Exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Middlewares
app.add_middleware(
    middleware_class=AuthMiddleware,
    admin_urls=(
        "/api/docs*",
        "/api/redoc*",
        "/api/openapi*",
    ),
)
app.add_middleware(
    middleware_class=LoggingMiddleware,
    exclude_requests=(
        ExcludedLogRequest(
            method="GET",
            path="/health/check*",
            host="127.0.0.1",
        ),
    ),
)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.add_middleware(
    middleware_class=ExceptionMiddleware,
    handlers=app.exception_handlers,
)
