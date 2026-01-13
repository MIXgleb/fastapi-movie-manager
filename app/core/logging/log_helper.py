from pathlib import Path

from loguru import logger

from app.core import settings
from app.core.logging.loggers import (
    common_logger,
    error_logger,
    intercept_logger,
    json_logger,
    stream_logger,
)


def setup_logger() -> None:
    """Initialize project logging."""
    log_folder = Path(settings.logging.log_folder).resolve()
    log_folder.mkdir(exist_ok=True, parents=True)

    logger.remove()

    intercept_logger.register()

    if settings.logging.stream.enabled:
        settings.logging.stream_log_handler = stream_logger.register()

    if settings.logging.common_file.enabled:
        settings.logging.common_log_handler = common_logger.register()

    if settings.logging.error_file.enabled:
        settings.logging.error_log_handler = error_logger.register()

    if settings.logging.json_file.enabled:
        settings.logging.json_log_handler = json_logger.register()

    logger.info("Logging setup completed successfully.")
