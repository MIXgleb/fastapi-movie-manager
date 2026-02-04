from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Required, TypedDict


class DictCustomRequestValidationError(TypedDict):
    """Typed dict."""

    loc: Sequence[str]
    msg: str
    type: str


class DictUrlParams(TypedDict, total=False):
    """Typed dict."""

    method: Required[str]
    path: Required[str]
    params: dict[str, Any]
    query: dict[str, str | list[str]]
    body: Any


@dataclass(slots=True, frozen=True)
class ExcludedLogRequest:
    """Request parameters."""

    method: str = "*"
    path: str = "*"
    host: str = "*"
