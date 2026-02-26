from fastapi import (
    FastAPI,
)
from fastapi.exceptions import (
    RequestValidationError,
)
from sqlalchemy.exc import (
    SQLAlchemyError,
)
from starlette.exceptions import (
    HTTPException,
)

from app.api import (
    router as api_router,
)
from app.core import (
    settings,
)
from app.core.config import (
    DEBUG,
)
from app.core.exceptions.exc_handlers import (
    DatabaseExceptionHandler,
    GlobalExceptionHandler,
    HTTPExceptionHandler,
    ValidationExceptionHandler,
)
from app.core.middlewares import (
    AuthMiddleware,
    CORSMiddleware,
    ExceptionMiddleware,
    LoggingMiddleware,
)
from app.core.typing_ import (
    ExcludedLogRequest,
)
from app.lifespan import (
    lifespan,
)
from app.security.auth_managers import (
    AuthJWTManager,
)

# ===========================================================================
# FastAPI application
# ===========================================================================
app = FastAPI(
    debug=DEBUG,
    title=settings.app.title,
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
    router=api_router,
)

# ===========================================================================
# Exception handlers
# ===========================================================================
app.add_exception_handler(
    exc_class_or_status_code=Exception,
    handler=GlobalExceptionHandler(),
)
app.add_exception_handler(
    exc_class_or_status_code=SQLAlchemyError,
    handler=DatabaseExceptionHandler(),
)
app.add_exception_handler(
    exc_class_or_status_code=HTTPException,
    handler=HTTPExceptionHandler(),
)
app.add_exception_handler(
    exc_class_or_status_code=RequestValidationError,
    handler=ValidationExceptionHandler(),
)

# ===========================================================================
# Middlewares
# ===========================================================================
app.add_middleware(
    middleware_class=AuthMiddleware,
    auth_manager=AuthJWTManager(
        auth_config=settings.auth_token,
    ),
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
