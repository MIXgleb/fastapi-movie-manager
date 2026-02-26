from typing import (
    final,
    override,
)

from loguru import (
    logger,
)

from app.core.config import (
    DEBUG,
)
from app.core.logging_.loggers.base import (
    BaseLogger,
)


@final
class ErrorLogger(BaseLogger):
    """Error file logger."""

    @override
    def register(self) -> int:
        return logger.add(
            sink=self.logger_config.path,
            level=self.logger_config.level,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
                "{level: <8} | "
                "{name}:{function}:{line} - {message}"
            ),
            rotation=self.logger_config.rotation,
            retention=self.logger_config.retention,
            compression="zip",
            encoding="utf-8",
            backtrace=True,
            enqueue=True,
            diagnose=DEBUG,
        )
