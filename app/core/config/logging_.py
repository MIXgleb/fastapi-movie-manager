from pydantic import (
    BaseModel as BaseSchema,
)
from pydantic.functional_validators import (
    field_validator,
)


class LoggerConfig(BaseSchema):
    """Logger configuration."""

    enabled: bool = False
    level: str = "INFO"
    path: str = "logs/{time:YYYY-MM-DD}/log.log"
    rotation: str = "00:00"
    retention: str = "30 days"

    @field_validator("level")
    @classmethod
    def validate_level(
        cls,
        level: str,
    ) -> str:
        """
        Validate level name.

        Parameters
        ----------
        level : str
            level name

        Returns
        -------
        str
            formatted level name

        Raises
        ------
        ValueError
            incorrect level name
        """
        valid_levels = {
            "TRACE",
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }

        if level.upper() not in valid_levels:
            exc_msg = f"Invalid log level. Must be one of: {valid_levels}"
            raise ValueError(exc_msg)

        return level.upper()


class LoggingConfig(BaseSchema):
    """Logging configuration."""

    log_folder: str = "logs"

    stream: LoggerConfig
    common_file: LoggerConfig
    error_file: LoggerConfig
    json_file: LoggerConfig

    stream_log_handler: int | None = None
    common_log_handler: int | None = None
    error_log_handler: int | None = None
    json_log_handler: int | None = None
