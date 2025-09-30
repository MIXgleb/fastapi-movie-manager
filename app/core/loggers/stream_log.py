import sys

from loguru import logger

from app.core.config import settings


def setup_stream_log() -> int:
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
