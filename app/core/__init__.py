__all__ = (
    "DEBUG",
    "settings",
)

from typing import Final

from app.core.config import settings

DEBUG: Final[bool] = settings.debug
