import logging
from collections.abc import (
    Sequence,
)
from typing import (
    final,
    override,
)

from app.core.logging_.intercept_handler import (
    InterceptHandler,
)
from app.core.logging_.loggers.base import (
    BaseLogger,
)


@final
class InterceptLogger(BaseLogger):
    """Interception logger."""

    __slots__ = ("disabled_loggers", "external_loggers")

    @override
    def __init__(
        self,
        external_loggers: Sequence[str],
        disabled_loggers: Sequence[str],
    ) -> None:
        """
        Initialize the intercept logger.

        Parameters
        ----------
        external_loggers : Sequence[str]
            name of the external loggers for interception

        disabled_loggers : Sequence[str]
            name of the disabled loggers for interception
        """
        self.external_loggers = external_loggers
        self.disabled_loggers = disabled_loggers

    @override
    def register(self) -> None:
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=0,
            force=True,
        )

        for log_name in self.external_loggers:
            logging_logger = logging.getLogger(log_name)
            logging_logger.handlers = [InterceptHandler()]
            logging_logger.propagate = False

        for log_name in self.disabled_loggers:
            logging_logger = logging.getLogger(log_name)
            logging_logger.disabled = True
