from typing import final, override

from fastapi import Request, Response
from loguru import logger

from app.core.exceptions.exc_handlers.base import (
    RESPONSE_JSON_500,
    BaseExceptionHandler,
)


@final
class GlobalExceptionHandler(BaseExceptionHandler):
    @override
    async def __call__(
        self,
        request: Request,
        exc: Exception,
    ) -> Response:
        method = request.method
        path = str(request.url)
        client = request.client
        client_ip = client.host if client is not None else "unknown"

        logger.bind(
            type="unexpected_exception",
            path=path,
            method=method,
            client_ip=client_ip,
            headers=request.headers,
        ).error(
            "UnexpectedException: {exc_msg};\nRequest: {method} {path}",
            exc_msg=repr(exc),
            method=method,
            path=path,
        )
        return RESPONSE_JSON_500
