import sys
from typing import (
    final,
    override,
)

from loguru import (
    logger,
)

from app.core.logging_.loggers.base import (
    BaseLogger,
)


@final
class StreamLogger(BaseLogger):
    """Stream stdout logger."""

    @override
    def register(self) -> int:
        return logger.add(
            sink=sys.stdout,
            level=self.logger_config.level,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            ),
            colorize=True,
        )
