from typing import (
    final,
    override,
)

from loguru import (
    logger,
)

from app.core.logging_.loggers.base import (
    BaseLogger,
)


@final
class JSONLogger(BaseLogger):
    """JSON file logger."""

    @override
    def register(self) -> int:
        return logger.add(
            sink=self.logger_config.path,
            level=self.logger_config.level,
            format="{message}",
            rotation=self.logger_config.rotation,
            retention=self.logger_config.retention,
            compression="zip",
            encoding="utf-8",
            serialize=True,
            enqueue=True,
        )
