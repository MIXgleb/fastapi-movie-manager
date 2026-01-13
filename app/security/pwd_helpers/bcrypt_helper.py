from typing import final, override

from passlib.context import CryptContext

from app.security.pwd_helpers.base import BasePasswordHelper


@final
class BcryptPasswordHelper(BasePasswordHelper):
    pwd_context = CryptContext(schemes=["bcrypt"])

    @classmethod
    @override
    def verify(
        cls,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    @override
    def hash(
        cls,
        password: str,
    ) -> str:
        return cls.pwd_context.hash(password)
