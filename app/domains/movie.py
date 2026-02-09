from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)


@dataclass(slots=True)
class MovieDM:
    id: int
    title: str
    description: str
    rate: float
    user_id: int
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class MovieFilterDM:
    limit: int
    offset: int
    sort_by: str
    rate_from: float
    rate_to: float
    title_contains: str | None
