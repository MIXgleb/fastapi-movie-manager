import traceback
from typing import (
    final,
    override,
)

from fastapi import (
    Request,
    Response,
)
from fastapi.responses import (
    JSONResponse,
)
from loguru import (
    logger,
)
from starlette.exceptions import (
    HTTPException,
)

from app.core.constants import (
    HTTP_RESPONSE_500,
)
from app.core.exceptions.exc_handlers.base import (
    BaseExceptionHandler,
)


@final
class HTTPExceptionHandler(BaseExceptionHandler):
    """
    HTTP exception handler.

    Exceptions:
        starlette.exceptions.HTTPException
    """

    @override
    async def __call__(
        self,
        request: Request,
        exc: Exception,
    ) -> Response:
        method, path, address = self._get_request_params(request)

        logger_fastapi_exc = logger.bind(
            path=path,
            method=method,
            address=address,
        )

        if isinstance(exc, HTTPException):
            logger_fastapi_exc.bind(
                type="http_exception",
                status_code=exc.status_code,
            ).warning(
                "HTTPException {status_code}: {exc_msg};\nRequest: {method} {path}",
                status_code=exc.status_code,
                exc_msg=(f"{exc.detail}\n{traceback.format_exc()}"),
                method=method,
                path=path,
            )
            return JSONResponse(
                content={
                    "error": exc.detail,
                },
                status_code=exc.status_code,
            )

        logger_fastapi_exc.bind(
            type="unexpected_exception",
        ).error(
            "UnexpectedException: {exc_msg};\nRequest: {method} {path}",
            exc_msg=(f"{exc!r}\n{traceback.format_exc()}"),
            method=method,
            path=path,
        )
        return HTTP_RESPONSE_500
