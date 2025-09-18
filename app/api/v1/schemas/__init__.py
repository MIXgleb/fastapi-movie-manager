__all__ = (
    "MessageDeleteMovieReturn",
    "MessageDeleteUserReturn",
    "MessageHealthCheckReturn",
    "MessageLoginReturn",
    "MessageRegisterReturn",
    "MessageUpdateMovieReturn",
)


from app.api.v1.schemas.auth import MessageLoginReturn, MessageRegisterReturn
from app.api.v1.schemas.health import MessageHealthCheckReturn
from app.api.v1.schemas.movie import MessageDeleteMovieReturn, MessageUpdateMovieReturn
from app.api.v1.schemas.user import MessageDeleteUserReturn
