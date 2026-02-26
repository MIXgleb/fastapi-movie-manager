from typing import (
    final,
)

from starlette.middleware.exceptions import (
    ExceptionMiddleware as BaseExceptionMiddleware,
)


@final
class ExceptionMiddleware(BaseExceptionMiddleware):
    """
    Middleware for handling exceptions.

    Parameters
    ----------
    handlers : Mapping[Any, ExceptionHandler] | None, optional
        Mapping of exception types to handler functions, \
            by default None
    """
