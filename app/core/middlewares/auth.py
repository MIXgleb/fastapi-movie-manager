from collections.abc import (
    Sequence,
)
from fnmatch import (
    fnmatch,
)
from functools import (
    lru_cache,
)
from typing import (
    final,
    override,
)

from fastapi import (
    Request,
    Response,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.types import (
    ASGIApp,
)

from app.security import (
    token_helper,
)


@final
class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for verifying user authentication.

    Parameters
    ----------
    admin_urls : Sequence[str], optional
        URLs accessible only to the admin \
            (wildcard is available), by default ()
    """

    __slots__ = ("admin_urls",)

    def __init__(
        self,
        app: ASGIApp,
        admin_urls: Sequence[str] = (),
    ) -> None:
        self.admin_urls = admin_urls
        super().__init__(app=app)

    @override
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        path = request.url.path

        tokens = await token_helper.validate_tokens(request)
        await token_helper.store_payload(tokens, request)
        await token_helper.store_tokens(tokens, request)

        if self._matches_path_with_admin_urls(path, self.admin_urls):
            await token_helper.check_admin_rights(request)

        response = await call_next(request)

        await token_helper.save_tokens(request, response)
        return response

    @staticmethod
    @lru_cache(maxsize=1024)
    def _matches_path_with_admin_urls(
        path: str,
        admin_urls: Sequence[str],
    ) -> bool:
        return any(fnmatch(path, url) for url in admin_urls)
