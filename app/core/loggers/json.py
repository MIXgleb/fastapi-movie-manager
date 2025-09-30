from loguru import logger

from app.core.config import settings


def setup_json_log() -> int:
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
