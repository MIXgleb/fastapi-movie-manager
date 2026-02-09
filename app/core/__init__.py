__all__ = (
    "DEBUG",
    "dep_rate_limiter_getter",
    "settings",
)

from typing import (
    Final,
)

from app.core.config import (
    settings,
)
from app.core.limiter import (
    dep_rate_limiter_getter,
)

DEBUG: Final[bool] = settings.debug
