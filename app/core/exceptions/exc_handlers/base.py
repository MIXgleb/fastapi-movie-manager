from abc import ABC, abstractmethod

from fastapi import Request, Response, status
from fastapi.responses import ORJSONResponse

RESPONSE_JSON_500 = ORJSONResponse(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    content={
        "error": "Internal server error.",
        "message": "Please try again later.",
    },
)


class BaseExceptionHandler(ABC):
    @abstractmethod
    def __call__(
        self,
        request: Request,
        exc: Exception,
    ) -> Response:
        """FastAPI exception handler.

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
