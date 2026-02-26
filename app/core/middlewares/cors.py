from typing import (
    final,
)

from fastapi.middleware.cors import (
    CORSMiddleware as BaseCORSMiddleware,
)


@final
class CORSMiddleware(BaseCORSMiddleware):
    """
    Middleware for handling Cross-Origin Resource Sharing (CORS).

    Parameters
    ----------
    allow_origins : Sequence[str], optional
        Allowed origins. '*' for all, by default ()

    allow_methods : Sequence[str], optional
        Allowed http methods. '*' for all, by default ("GET",)

    allow_headers : Sequence[str], optional
        Allowed headers. '*' for all, by default ()

    allow_credentials : bool, optional
        Allow cookies/credentials, by default False

    allow_origin_regex : str | None, optional
        Regex pattern for matching allowed origins, by default None

    expose_headers : Sequence[str], optional
        Headers exposed to browser JavaScript, by default ()

    max_age : int, optional
        Preflight result cache time in seconds, by default 600
    """
