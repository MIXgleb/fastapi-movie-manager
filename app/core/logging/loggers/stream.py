import sys
from typing import (
    final,
    override,
)

from loguru import (
    logger,
)

from app.core import (
    settings,
)
from app.core.logging.loggers.base import (
    BaseLogger,
)


@final
class StreamLogger(BaseLogger):
    @classmethod
    @override
    def register(cls) -> int:
        return logger.add(
            sink=sys.stdout,
            level=settings.logging.stream.level,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            ),
            colorize=True,
        )
