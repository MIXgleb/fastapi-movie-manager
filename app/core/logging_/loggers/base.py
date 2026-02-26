from abc import (
    ABC,
    abstractmethod,
)

from app.core.config import (
    LoggerConfig,
)


class BaseLogger(ABC):
    """Basic abstract logger class."""

    __slots__ = ("logger_config",)

    def __init__(
        self,
        logger_config: LoggerConfig,
    ) -> None:
        """
        Initialize the logger.

        Parameters
        ----------
        logger_config : LoggerConfig
            logger config
        """
        self.logger_config = logger_config

    @abstractmethod
    def register(self) -> int | None:
        """
        Register a new logger.

        Returns
        -------
        int | None
            logger number
        """
        raise NotImplementedError
