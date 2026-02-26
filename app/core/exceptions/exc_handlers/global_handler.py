import traceback
from typing import (
    final,
    override,
)

from fastapi import (
    Request,
    Response,
)
from loguru import (
    logger,
)

from app.core.constants import (
    HTTP_RESPONSE_500,
)
from app.core.exceptions.exc_handlers.base import (
    BaseExceptionHandler,
)


@final
class GlobalExceptionHandler(BaseExceptionHandler):
    """
    Global exception handler.

    Exceptions:
        All
    """

    @override
    async def __call__(
        self,
        request: Request,
        exc: Exception,
    ) -> Response:
        method, path, address = self._get_request_params(request)

        logger.bind(
            type="unexpected_exception",
            path=path,
            method=method,
            address=address,
        ).error(
            "UnexpectedException: {exc_msg};\nRequest: {method} {path}",
            exc_msg=(f"{exc!r}\n{traceback.format_exc()}"),
            method=method,
            path=path,
        )
        return HTTP_RESPONSE_500
