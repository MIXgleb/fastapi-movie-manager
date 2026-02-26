import traceback
from collections.abc import (
    Sequence,
)
from typing import (
    Any,
    final,
    override,
)

from fastapi import (
    Request,
    Response,
    status,
)
from fastapi.exceptions import (
    RequestValidationError,
)
from fastapi.responses import (
    JSONResponse,
)
from loguru import (
    logger,
)
from pydantic import (
    BaseModel as BaseSchema,
)
from pydantic.fields import (
    Field,
)

from app.core.constants import (
    HTTP_RESPONSE_500,
)
from app.core.exceptions.exc_handlers.base import (
    BaseExceptionHandler,
)
from app.core.typing_ import (
    DictUrlParams,
)


class _ValidationErrorSchema(BaseSchema):
    field: Sequence[Any]
    message: str
    extra_message: dict[Any, Any]
    type: str


class _ProblemDetailsSchema(BaseSchema):
    type: str = Field(default="about:blank")
    title: str
    status: int
    detail: str
    instance: DictUrlParams
    errors: list[_ValidationErrorSchema]


@final
class ValidationExceptionHandler(BaseExceptionHandler):
    """
    Validation exception handler.

    Exceptions:
        fastapi.exceptions.RequestValidationError
    """

    @override
    async def __call__(
        self,
        request: Request,
        exc: Exception,
    ) -> Response:
        method, path, address = self._get_request_params(request)

        logger_validation_exc = logger.bind(
            path=path,
            method=method,
            address=address,
        )

        if isinstance(exc, RequestValidationError):
            problem_details = _ProblemDetailsSchema(
                title="Validation Error",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="One or more validation errors occurred in the request.",
                instance=self._get_full_url_params(request, exc),
                errors=self._get_custom_error_descriptions(exc),
            )
            logger_validation_exc.bind(
                type="validation_exception",
            ).warning(
                "RequestValidationError: {exc_msg};\nRequest: {method} {path}",
                exc_msg=problem_details.model_dump_json(),
                method=method,
                path=path,
            )
            return JSONResponse(
                content=problem_details.model_dump(),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                headers={"Content-Type": "application/problem+json"},
            )

        logger_validation_exc.bind(
            type="unexpected_exception",
        ).error(
            "UnexpectedException: {exc_msg};\nRequest: {method} {path}",
            exc_msg=(f"{exc!r}\n{traceback.format_exc()}"),
            method=method,
            path=path,
        )
        return HTTP_RESPONSE_500

    @classmethod
    def _get_custom_error_descriptions(
        cls,
        exc: RequestValidationError,
    ) -> list[_ValidationErrorSchema]:
        return [
            _ValidationErrorSchema(
                field=error.get("loc", []),
                message=error.get("msg", ""),
                extra_message=error.get("ctx", {}),
                type=error.get("type", ""),
            )
            for error in exc.errors()
        ]

    @classmethod
    def _get_full_url_params(
        cls,
        request: Request,
        exc: RequestValidationError,
    ) -> DictUrlParams:
        instance = DictUrlParams(
            method=request.method,
            path=request.url.path,
        )

        if path_params := request.path_params:
            instance["params"] = path_params

        if query_params := request.query_params:
            dict_query: dict[str, str | list[str]] = {}

            for q in str(query_params).split("&"):
                k, v = q.split("=")

                if k in dict_query:
                    cur = dict_query[k]
                    dict_query[k] = [*cur, v] if isinstance(cur, list) else [cur, v]
                else:
                    dict_query[k] = v

            instance["query"] = dict_query

        body_key = "body"

        if hasattr(exc, body_key) and getattr(exc, body_key):
            instance["body"] = getattr(exc, body_key)

        return instance
