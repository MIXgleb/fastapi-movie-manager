from abc import ABC, abstractmethod
from typing import ClassVar, final, override

from passlib.context import CryptContext


class PasswordHelperBase(ABC):
    pwd_context: ClassVar

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


@final
class BcryptPasswordHelper(PasswordHelperBase):
    pwd_context = CryptContext(schemes=["bcrypt"])

    @classmethod
    @override
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    @override
    def hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)
