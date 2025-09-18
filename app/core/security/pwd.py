from abc import ABC, abstractmethod
from typing import override

from passlib.context import CryptContext


class PasswordHelperBase[Context](ABC):
    context: Context

    @classmethod
    @abstractmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
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
    def hash(cls, password: str) -> str:
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


class BcryptPasswordHelper(PasswordHelperBase[CryptContext]):
    context = CryptContext(schemes=["bcrypt"])

    @classmethod
    @override
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.context.verify(plain_password, hashed_password)

    @classmethod
    @override
    def hash(cls, password: str) -> str:
        return cls.context.hash(password)
