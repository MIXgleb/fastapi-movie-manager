from abc import (
    ABC,
    abstractmethod,
)

from app.core.typing_ import (
    ArgsType,
    KwargsType,
)


class BaseDependency(ABC):
    """Basic abstract dependency class."""

    @abstractmethod
    async def __call__(
        self,
        *args: ArgsType,
        **kwargs: KwargsType,
    ) -> None:
        """Endpoint-level dependency."""
        raise NotImplementedError
