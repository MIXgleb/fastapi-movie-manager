from loguru import logger

from app.core.config import DEBUG, settings


def setup_error_log() -> int:
    return logger.add(
        sink=settings.logging.error_file.path,
        level=settings.logging.error_file.level,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} - {message}"
        ),
        rotation=settings.logging.error_file.rotation,
        retention=settings.logging.error_file.retention,
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        enqueue=True,
        diagnose=DEBUG,
    )
