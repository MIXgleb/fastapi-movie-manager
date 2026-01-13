__all__ = (
    "common_logger",
    "error_logger",
    "intercept_logger",
    "json_logger",
    "stream_logger",
)


from app.core.logging.loggers.common import CommonLogger
from app.core.logging.loggers.error import ErrorLogger
from app.core.logging.loggers.intercept import InterceptLogger
from app.core.logging.loggers.json import JSONLogger
from app.core.logging.loggers.stream import StreamLogger

common_logger = CommonLogger()
error_logger = ErrorLogger()
intercept_logger = InterceptLogger()
json_logger = JSONLogger()
stream_logger = StreamLogger()
