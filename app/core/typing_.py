from collections.abc import (
    Sequence,
)
from dataclasses import (
    dataclass,
)
from typing import (
    Any,
    Required,
    TypedDict,
)

type DictAnyAnyType = dict[Any, Any]
type ArgsType = Any
type KwargsType = Any


class DictRequestValidationError(TypedDict):
    """Typed dictionary of request validation error."""

    loc: Sequence[str]
    msg: str
    type: str


class DictUrlParams(TypedDict, total=False):
    """Typed dictionary of url parameters."""

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
