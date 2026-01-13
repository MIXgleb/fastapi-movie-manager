import logging
from typing import final, override

from app.core.logging.interceptions import InterceptionHandler
from app.core.logging.loggers.base import BaseLogger


@final
class InterceptLogger(BaseLogger):
    @classmethod
    @override
    def register(cls) -> None:
        logging.basicConfig(
            handlers=[InterceptionHandler()],
            level=0,
            force=True,
        )
