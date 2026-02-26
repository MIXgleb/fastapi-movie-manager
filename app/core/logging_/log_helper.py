from collections.abc import (
    Sequence,
)
from pathlib import (
    Path,
)

from loguru import (
    logger,
)

from app.core.config import (
    LoggingConfig,
)
from app.core.logging_.loggers import (
    CommonLogger,
    ErrorLogger,
    InterceptLogger,
    JSONLogger,
    StreamLogger,
)


def setup_logger(
    logging_config: LoggingConfig,
    external_loggers: Sequence[str] = (),
    disabled_loggers: Sequence[str] = (),
) -> None:
    """
    Initialize project logging.

    Parameters
    ----------
    logging_config : LoggingConfig
        logging config

    external_loggers : Sequence[str], optional
        name of the external loggers for interception, \
            by default ()

    disabled_loggers : Sequence[str], optional
        name of the disabled loggers for interception, \
            by default ()
    """
    log_folder = Path(logging_config.log_folder).resolve()
    log_folder.mkdir(exist_ok=True, parents=True)

    logger.remove()

    InterceptLogger(
        external_loggers=external_loggers,
        disabled_loggers=disabled_loggers,
    ).register()

    if logging_config.stream.enabled:
        logging_config.stream_log_handler = StreamLogger(
            logger_config=logging_config.stream,
        ).register()

    if logging_config.common_file.enabled:
        logging_config.common_log_handler = CommonLogger(
            logger_config=logging_config.common_file,
        ).register()

    if logging_config.error_file.enabled:
        logging_config.error_log_handler = ErrorLogger(
            logger_config=logging_config.error_file,
        ).register()

    if logging_config.json_file.enabled:
        logging_config.json_log_handler = JSONLogger(
            logger_config=logging_config.json_file,
        ).register()

    logger.info("Logging setup completed successfully.")
