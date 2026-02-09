from fastapi import (
    FastAPI,
)
from fastapi.exceptions import (
    RequestValidationError,
)
from fastapi.responses import (
    ORJSONResponse,
)
from sqlalchemy.exc import (
    SQLAlchemyError,
)
from starlette.exceptions import (
    HTTPException,
)

from app.api import (
    api_v1_router,
    internal_router,
)
from app.core import (
    DEBUG,
    settings,
)
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
from app.core.typing import (
    ExcludedLogRequest,
)
from app.lifespan import (
    lifespan,
)

# ===========================================================================
# FastAPI application
# ===========================================================================
app = FastAPI(
    debug=DEBUG,
    title="FastAPI movies",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    openapi_url=f"{settings.api.internal.prefix}/openapi.json",
    docs_url=f"{settings.api.internal.prefix}/docs",
    redoc_url=f"{settings.api.internal.prefix}/redoc",
    root_path="",
)

# ===========================================================================
# Routers
# ===========================================================================
app.include_router(
    router=internal_router,
    prefix=settings.api.internal.prefix,
)
app.include_router(
    router=api_v1_router,
    prefix=settings.api.prefix,
)

# ===========================================================================
# Exception handlers
# ===========================================================================
app.add_exception_handler(
    exc_class_or_status_code=Exception,
    handler=global_exception_handler,
)
app.add_exception_handler(
    exc_class_or_status_code=SQLAlchemyError,
    handler=database_exception_handler,
)
app.add_exception_handler(
    exc_class_or_status_code=HTTPException,
    handler=http_exception_handler,
)
app.add_exception_handler(
    exc_class_or_status_code=RequestValidationError,
    handler=validation_exception_handler,
)

# ===========================================================================
# Middlewares
# ===========================================================================
app.add_middleware(
    middleware_class=AuthMiddleware,
    admin_urls=(
        f"{settings.api.internal.prefix}/docs*" if not DEBUG else "",
        f"{settings.api.internal.prefix}/redoc*" if not DEBUG else "",
        f"{settings.api.internal.prefix}/openapi*" if not DEBUG else "",
    ),
)
app.add_middleware(
    middleware_class=LoggingMiddleware,
    exclude_requests=(
        ExcludedLogRequest(
            method="GET",
            path=f"{settings.api.internal.prefix}/*",
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
