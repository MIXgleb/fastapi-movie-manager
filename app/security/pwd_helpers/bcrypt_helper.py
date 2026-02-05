from typing import final, override

import bcrypt

from app.security.pwd_helpers.base import BasePasswordHelper


@final
class BcryptPasswordHelper(BasePasswordHelper):
    @classmethod
    @override
    def verify(
        cls,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return bcrypt.checkpw(
            password=plain_password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8"),
        )

    @classmethod
    @override
    def hash(
        cls,
        password: str,
    ) -> str:
        return bcrypt.hashpw(
            password=password.encode("utf-8"),
            salt=bcrypt.gensalt(),
        ).decode("utf-8")
