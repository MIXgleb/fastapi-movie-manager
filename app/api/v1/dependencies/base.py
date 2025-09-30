from abc import ABC, abstractmethod
from typing import Annotated, Any

from fastapi import Depends

from app.core.security import Payload, TokenHelper

PayloadByToken = Annotated[Payload, Depends(TokenHelper())]


class EndpointDependencyBase(ABC):
    @abstractmethod
    async def __call__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Endpoint-level dependency."""
        raise NotImplementedError
