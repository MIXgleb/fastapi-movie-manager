from typing import final, override

from fastapi import HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions.exc_handlers.base import (
    RESPONSE_JSON_500,
    BaseExceptionHandler,
)


@final
class HTTPExceptionHandler(BaseExceptionHandler):
    @override
    def __call__(
        self,
        request: Request,
        exc: Exception,
    ) -> Response:
        method = request.method
        path = str(request.url)
        client = request.client
        client_ip = client.host if client is not None else "unknown"

        logger_fastapi_exc = logger.bind(
            path=path,
            method=method,
            client_ip=client_ip,
            headers=request.headers,
        )

        if isinstance(exc, HTTPException):
            logger_fastapi_exc.bind(
                type="http_exception",
                status_code=exc.status_code,
            ).warning(
                "HTTPException {status_code}: {exc_msg};\nRequest: {method} {path}",
                status_code=exc.status_code,
                exc_msg=exc.detail,
                method=method,
                path=path,
            )
            return ORJSONResponse(
                status_code=exc.status_code,
                content=jsonable_encoder({"error": exc.detail}),
            )

        logger_fastapi_exc.bind(type="unexpected_exception").error(
            "UnexpectedException: {exc_msg};\nRequest: {method} {path}",
            exc_msg=repr(exc),
            method=method,
            path=path,
        )
        return RESPONSE_JSON_500


@final
class DatabaseExceptionHandler(BaseExceptionHandler):
    @override
    def __call__(
        self,
        request: Request,
        exc: Exception,
    ) -> Response:
        method = request.method
        path = str(request.url)
        client = request.client
        client_ip = client.host if client is not None else "unknown"

        logger_db_exc = logger.bind(
            path=path,
            method=method,
            client_ip=client_ip,
            headers=request.headers,
        )

        if isinstance(exc, SQLAlchemyError):
            logger_db_exc.bind(type="sqlalchemy_exception").error(
                "SQLAlchemyException: {exc_msg};\nRequest: {method} {path}",
                exc_msg=repr(exc),
                method=method,
                path=path,
            )
            return RESPONSE_JSON_500

        logger_db_exc.bind(type="unexpected_exception").error(
            "UnexpectedException: {exc_msg};\nRequest: {method} {path}",
            exc_msg=repr(exc),
            method=method,
            path=path,
        )
        return RESPONSE_JSON_500
