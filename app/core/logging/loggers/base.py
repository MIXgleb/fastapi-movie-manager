from abc import ABC, abstractmethod


class BaseLogger(ABC):
    @classmethod
    @abstractmethod
    def register(cls) -> int | None:
        """Register a new logger.

        Returns
        -------
        int | None
            logger number
        """
        raise NotImplementedError
