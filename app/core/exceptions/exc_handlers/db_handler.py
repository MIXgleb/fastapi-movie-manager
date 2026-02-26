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
from sqlalchemy.exc import (
    SQLAlchemyError,
)

from app.core.constants import (
    HTTP_RESPONSE_500,
)
from app.core.exceptions.exc_handlers.base import (
    BaseExceptionHandler,
)


@final
class DatabaseExceptionHandler(BaseExceptionHandler):
    """
    Database exception handler.

    Exceptions:
        sqlalchemy.exc.SQLAlchemyError
    """

    @override
    async def __call__(
        self,
        request: Request,
        exc: Exception,
    ) -> Response:
        method, path, address = self._get_request_params(request)

        logger_db_exc = logger.bind(
            path=path,
            method=method,
            address=address,
        )

        if isinstance(exc, SQLAlchemyError):
            logger_db_exc.bind(
                type="sqlalchemy_exception",
            ).error(
                "SQLAlchemyException: {exc_msg};\nRequest: {method} {path}",
                exc_msg=(f"{exc!r}\n{traceback.format_exc()}"),
                method=method,
                path=path,
            )
            return HTTP_RESPONSE_500

        logger_db_exc.bind(
            type="unexpected_exception",
        ).error(
            "UnexpectedException: {exc_msg};\nRequest: {method} {path}",
            exc_msg=(f"{exc!r}\n{traceback.format_exc()}"),
            method=method,
            path=path,
        )
        return HTTP_RESPONSE_500
