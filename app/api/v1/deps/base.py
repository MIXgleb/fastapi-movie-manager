from abc import ABC, abstractmethod
from typing import Any


class EndpointDependencyBase(ABC):
    @abstractmethod
    async def __call__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Endpoint-level dependency."""
        raise NotImplementedError
