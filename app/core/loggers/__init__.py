__all__ = ("setup_logger",)


from loguru import logger

from app.core.config import settings
from app.core.loggers.common import setup_common_log
from app.core.loggers.error import setup_error_log
from app.core.loggers.interception import setup_interception_log
from app.core.loggers.json import setup_json_log
from app.core.loggers.stream import setup_stream_log


def setup_logger() -> None:
    setup_interception_log()

    if settings.logging.stream.enabled:
        settings.logging.stream_log_handler = setup_stream_log()

    if settings.logging.common_file.enabled:
        settings.logging.common_log_handler = setup_common_log()

    if settings.logging.error_file.enabled:
        settings.logging.error_log_handler = setup_error_log()

    if settings.logging.json_file.enabled:
        settings.logging.json_log_handler = setup_json_log()

    logger.info("Logging setup completed successfully.")
