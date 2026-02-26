import logging
from typing import (
    TYPE_CHECKING,
    final,
    override,
)

from loguru import (
    logger,
)

if TYPE_CHECKING:
    from types import (
        FrameType,
    )


@final
class InterceptHandler(logging.Handler):
    """Handler for intercepting external loggers."""

    @override
    def emit(
        self,
        record: logging.LogRecord,
    ) -> None:
        level: str | int
        frame: FrameType | None

        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2

        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            exception=record.exc_info,
            depth=depth,
        ).log(level, record.getMessage())
