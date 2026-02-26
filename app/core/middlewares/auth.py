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
    Any,
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

from app.security.auth_managers import (
    BaseAuthManager,
)


@final
class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware for verifying user authentication.

    Parameters
    ----------
    auth_manager : BaseAuthManager
        auth manager

    admin_urls : Sequence[str], optional
        URLs accessible only to the admin \
            (wildcard is available), by default ()
    """

    __slots__ = ("admin_urls", "auth_manager")

    @override
    def __init__(
        self,
        app: ASGIApp,
        auth_manager: BaseAuthManager[Any, Any, Any, Any, Any],
        admin_urls: Sequence[str] = (),
    ) -> None:
        super().__init__(app=app)
        self.auth_manager = auth_manager
        self.admin_urls = admin_urls

    @override
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        path = request.url.path

        tokens = await self.auth_manager.validate_tokens(request)
        await self.auth_manager.store_payload(tokens, request)
        await self.auth_manager.store_tokens(tokens, request)

        if self._matches_path_with_admin_urls(path, self.admin_urls):
            await self.auth_manager.check_admin_rights(request)

        response = await call_next(request)

        await self.auth_manager.save_tokens(request, response)
        return response

    @staticmethod
    @lru_cache(maxsize=1024)
    def _matches_path_with_admin_urls(
        path: str,
        admin_urls: Sequence[str],
    ) -> bool:
        return any(fnmatch(path, url) for url in admin_urls)
