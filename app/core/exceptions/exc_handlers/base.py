from abc import (
    ABC,
    abstractmethod,
)

from fastapi import (
    Request,
    Response,
)

type Method = str
type Path = str
type Address = str


class BaseExceptionHandler(ABC):
    """Basic abstract exception handler class."""

    @abstractmethod
    async def __call__(
        self,
        request: Request,
        exc: Exception,
    ) -> Response:
        """
        FastAPI exception handler.

        Parameters
        ----------
        request : Request
            request from the client

        exc : Exception
            caught exception

        Returns
        -------
        Response
            response to the client
        """
        raise NotImplementedError

    @classmethod
    def _get_request_params(
        cls,
        request: Request,
    ) -> tuple[Method, Path, Address]:
        method = request.method
        path = str(request.url)
        address_params = request.client
        address = (
            f"{address_params.host}:{address_params.port}"
            if address_params is not None
            else "unknown"
        )
        return method, path, address
