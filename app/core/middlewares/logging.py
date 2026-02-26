import time
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
from loguru import (
    logger,
)
from starlette.datastructures import (
    Address as Client,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.types import (
    ASGIApp,
)

from app.core.typing_ import (
    ExcludedLogRequest,
)

type Method = str
type Path = str
type Address = str


@final
class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.

    Parameters
    ----------
    exclude_requests : Sequence[ExcludedLogRequest], optional
        Requests to exclude from logging based \
            (wildcard is available), by default ()

    """

    __slots__ = ("excluded_requests",)

    @override
    def __init__(
        self,
        app: ASGIApp,
        exclude_requests: Sequence[ExcludedLogRequest] = (),
    ) -> None:
        super().__init__(app=app)
        self.excluded_requests = self._convert_excluded_requests_to_tuple_str(exclude_requests)

    @override
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time.time()
        method, path, address = self._get_request_params(request)
        is_excluded = self._matches_request_with_excluded(
            method=method,
            path=path,
            client=request.client,
            excluded_requests=self.excluded_requests,
        )

        logger_request = logger.bind(
            path=path,
            method=method,
            address=address,
        )

        if not is_excluded:
            logger_request.bind(
                type="request",
            ).info(
                "Request: {method} {path} from {address}",
                method=method,
                path=path,
                address=address,
            )

        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        if not is_excluded:
            logger_request.bind(
                type="response",
                process_time=str(process_time),
            ).info(
                "Response: {method} {path} returned {status_code} to {address}",
                method=method,
                path=path,
                status_code=response.status_code,
                address=address,
            )

        return response

    def _convert_excluded_requests_to_tuple_str(
        self,
        exclude_requests: Sequence[ExcludedLogRequest],
    ) -> tuple[str, ...]:
        return tuple(
            self._get_request_params_string(
                method=request.method,
                path=request.path,
                host=request.host,
            )
            for request in exclude_requests
        )

    @classmethod
    def _get_request_params(
        cls,
        request: Request,
    ) -> tuple[Method, Path, Address]:
        method = request.method
        path = request.url.path
        address_params = request.client
        address = (
            f"{address_params.host}:{address_params.port}"
            if address_params is not None
            else "unknown"
        )
        return method, path, address

    @staticmethod
    @lru_cache(maxsize=1024)
    def _get_request_params_string(
        method: str,
        path: str,
        host: str,
    ) -> str:
        return f"{method.upper()} {host.lower()} {path}"

    @staticmethod
    @lru_cache(maxsize=1024)
    def _matches_request_with_excluded(
        method: str,
        path: str,
        client: Client | None,
        excluded_requests: tuple[str, ...],
    ) -> bool:
        request = LoggingMiddleware._get_request_params_string(
            method=method,
            path=path,
            host=client.host if client else "*",
        )
        return any(fnmatch(request, ex_req) for ex_req in excluded_requests)
