from typing import final

from fastapi.middleware.cors import CORSMiddleware as BaseCORSMiddleware
from starlette.types import ASGIApp


@final
class CORSMiddleware(BaseCORSMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        allow_origins = ["*"]
        allow_methods = ["GET", "POST", "PUT", "DELETE"]
        allow_headers = ["*"]
        allow_credentials = True
        allow_origin_regex = None
        expose_headers = ()
        max_age = 600

        super().__init__(
            app=app,
            allow_origins=allow_origins,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
            allow_credentials=allow_credentials,
            allow_origin_regex=allow_origin_regex,
            expose_headers=expose_headers,
            max_age=max_age,
        )
