import logging
from collections.abc import Sequence
from typing import final, override

from app.core.logging.interceptions import InterceptHandler
from app.core.logging.loggers.base import BaseLogger


@final
class InterceptLogger(BaseLogger):
    @classmethod
    @override
    def register(
        cls,
        external_loggers: Sequence[str],
        disabled_loggers: Sequence[str],
    ) -> None:
        """Register a intercept logger.

        Parameters
        ----------
        external_loggers : Sequence[str]
            name of the external loggers for interception

        disabled_loggers : Sequence[str]
            name of the disabled loggers for interception
        """
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=0,
            force=True,
        )

        for log_name in external_loggers:
            logging_logger = logging.getLogger(log_name)
            logging_logger.handlers = [InterceptHandler()]
            logging_logger.propagate = False

        for log_name in disabled_loggers:
            logging_logger = logging.getLogger(log_name)
            logging_logger.disabled = True
