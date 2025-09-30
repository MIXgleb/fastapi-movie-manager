from typing import Any, Required, TypedDict

from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.core.exceptions.errors import CustomValidationErrorSchema


class DictUrlParams(TypedDict, total=False):
    method: Required[str]
    path: Required[str]
    params: dict[str, Any]
    query: dict[str, str | list[str]]
    body: Any


def get_custom_error_descriptions(
    exc: RequestValidationError,
) -> list[CustomValidationErrorSchema]:
    """Convert the default error descriptions to the custom type.

    Parameters
    ----------
    exc : RequestValidationError
        exception instance

    Returns
    -------
    list[CustomValidationErrorSchema]
        custom error description list
    """
    return [
        CustomValidationErrorSchema(
            field=error.get("loc", []),
            message=error.get("msg", ""),
            extra_message=error.get("ctx", {}),
            type=error.get("type", ""),
        )
        for error in exc.errors()
    ]


def get_full_url_params(request: Request, exc: Exception) -> DictUrlParams:
    """Get the full URL details.

    Parameters
    ----------
    request : Request
        request to the endpoint

    exc : Exception
        exception instance

    Returns
    -------
    DictUrlParams
        url instance params
    """
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
