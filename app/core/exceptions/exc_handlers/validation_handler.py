from collections.abc import Sequence
from typing import (
    Any,
    Required,
    TypedDict,
    final,
    override,
)

from fastapi import Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from loguru import logger
from pydantic import BaseModel, Field

from app.core.exceptions.exc_handlers.base import (
    RESPONSE_JSON_500,
    BaseExceptionHandler,
)


class _CustomValidationErrorSchema(BaseModel):
    field: Sequence[Any]
    message: str
    extra_message: dict[Any, Any]
    type: str


class _DictUrlParams(TypedDict, total=False):
    method: Required[str]
    path: Required[str]
    params: dict[str, Any]
    query: dict[str, str | list[str]]
    body: Any


class _CustomProblemDetailsSchema(BaseModel):
    type: str = Field(
        default="about:blank",
        description="A URI reference that identifies the problem type",
    )
    title: str
    status: int
    detail: str
    instance: _DictUrlParams
    errors: list[_CustomValidationErrorSchema]


@final
class ValidationExceptionHandler(BaseExceptionHandler):
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

        logger_validation_exc = logger.bind(
            path=path,
            method=method,
            client_ip=client_ip,
            headers=request.headers,
        )

        if isinstance(exc, RequestValidationError):
            problem_details = _CustomProblemDetailsSchema(
                title="Validation Error",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="One or more validation errors occurred in the request.",
                instance=self._get_full_url_params(request, exc),
                errors=self._get_custom_error_descriptions(exc),
            )
            logger_validation_exc.bind(type="validation_exception").warning(
                "RequestValidationError: {exc_msg};\nRequest: {method} {path}",
                exc_msg=problem_details.model_dump_json(),
                method=method,
                path=path,
            )
            return ORJSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=jsonable_encoder(problem_details),
                headers={"Content-Type": "application/problem+json"},
            )

        logger_validation_exc.bind(type="unexpected_exception").error(
            "UnexpectedException: {exc_msg};\nRequest: {method} {path}",
            exc_msg=repr(exc),
            method=method,
            path=path,
        )
        return RESPONSE_JSON_500

    @classmethod
    def _get_custom_error_descriptions(
        cls,
        exc: RequestValidationError,
    ) -> list[_CustomValidationErrorSchema]:
        return [
            _CustomValidationErrorSchema(
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
    ) -> _DictUrlParams:
        instance = _DictUrlParams(
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
