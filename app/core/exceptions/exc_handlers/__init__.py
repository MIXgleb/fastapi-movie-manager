__all__ = (
    "database_exception_handler",
    "global_exception_handler",
    "http_exception_handler",
    "validation_exception_handler",
)


from app.core.exceptions.exc_handlers.common_handlers import (
    DatabaseExceptionHandler,
    HTTPExceptionHandler,
)
from app.core.exceptions.exc_handlers.global_handler import (
    GlobalExceptionHandler,
)
from app.core.exceptions.exc_handlers.validation_handler import (
    ValidationExceptionHandler,
)

database_exception_handler = DatabaseExceptionHandler()
global_exception_handler = GlobalExceptionHandler()
http_exception_handler = HTTPExceptionHandler()
validation_exception_handler = ValidationExceptionHandler()
