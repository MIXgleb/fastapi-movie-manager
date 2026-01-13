from abc import ABC, abstractmethod
from typing import Any


class BaseDependency(ABC):
    @abstractmethod
    async def __call__(
        self,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Endpoint-level dependency."""
        raise NotImplementedError
