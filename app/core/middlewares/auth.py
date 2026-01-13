from collections.abc import Sequence
from fnmatch import fnmatch
from typing import final, override

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from app.security import TokenHelper


@final
class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        only_admin_urls: Sequence[str] = (),
    ) -> None:
        self.only_admin_urls = only_admin_urls
        super().__init__(app=app)

    @override
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        path = request.url.path

        tokens = await TokenHelper.validate_tokens(request)
        await TokenHelper.store_payload(tokens, request)
        await TokenHelper.store_tokens(tokens, request)

        if any(fnmatch(path, url) for url in self.only_admin_urls):
            await TokenHelper.check_admin_rights(request)

        response = await call_next(request)

        await TokenHelper.save_tokens(request, response)
        return response
