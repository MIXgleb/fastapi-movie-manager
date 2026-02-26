from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from uuid import (
    UUID,
)

from app.domains.base import (
    BaseDataclass,
)


@dataclass(slots=True, frozen=True)
class MovieInputDM(BaseDataclass):
    """Domain model of getting a movie."""

    title: str
    description: str
    rate: float


@dataclass(slots=True, frozen=True)
class MovieCreateDM(MovieInputDM):
    """Domain model of creating a movie."""

    user_id: UUID


@dataclass(slots=True, frozen=True)
class MovieUpdateDM(BaseDataclass):
    """Domain model of updating a movie."""

    title: str | None
    description: str | None
    rate: float | None


@dataclass(slots=True, frozen=True)
class MovieOutputDM(MovieCreateDM):
    """Domain model of returning a movie."""

    id: int | UUID
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True, frozen=True)
class MovieFiltersDM(BaseDataclass):
    """Domain model of filtering a movie."""

    limit: int
    offset: int
    sort_by: str
    rate_from: float
    rate_to: float
    title_contains: str | None
