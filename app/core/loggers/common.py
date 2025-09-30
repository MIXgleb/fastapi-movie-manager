from loguru import logger

from app.core.config import settings


def setup_common_log() -> int:
    return logger.add(
        sink=settings.logging.common_file.path,
        level=settings.logging.common_file.level,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} - {message}"
        ),
        rotation=settings.logging.common_file.rotation,
        retention=settings.logging.common_file.retention,
        compression="zip",
        encoding="utf-8",
        enqueue=True,
    )
