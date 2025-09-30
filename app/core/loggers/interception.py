import logging
from typing import override

from loguru import logger


class InterceptHandler(logging.Handler):
    @override
    def emit(self, record: logging.LogRecord) -> None:
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


def setup_interception_log() -> None:
    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=0,
        force=True,
    )
