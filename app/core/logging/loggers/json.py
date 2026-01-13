from typing import final, override

from loguru import logger

from app.core import settings
from app.core.logging.loggers.base import BaseLogger


@final
class JSONLogger(BaseLogger):
    @classmethod
    @override
    def register(cls) -> int:
        return logger.add(
            sink=settings.logging.json_file.path,
            level=settings.logging.json_file.level,
            format="{message}",
            rotation=settings.logging.json_file.rotation,
            retention=settings.logging.json_file.retention,
            compression="zip",
            encoding="utf-8",
            serialize=True,
            enqueue=True,
        )
