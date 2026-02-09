from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
)


class BaseLogger(ABC):
    @classmethod
    @abstractmethod
    def register(
        cls,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> int | None:
        """Register a new logger.

        Returns
        -------
        int | None
            logger number
        """
        raise NotImplementedError
