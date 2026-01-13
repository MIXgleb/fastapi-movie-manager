from abc import ABC, abstractmethod
from typing import ClassVar


class BasePasswordHelper(ABC):
    pwd_context: ClassVar

    @classmethod
    @abstractmethod
    def verify(
        cls,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """Password and hash verification.

        Parameters
        ----------
        plain_password : str
            user's password

        hashed_password : str
            hashed password

        Returns
        -------
        bool
            comparison status
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def hash(
        cls,
        password: str,
    ) -> str:
        """Hash the password.

        Parameters
        ----------
        password : str
            user's password

        Returns
        -------
        str
            hashed password
        """
        raise NotImplementedError
