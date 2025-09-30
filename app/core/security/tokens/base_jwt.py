from typing import Any

import jwt

from app.core.config import settings
from app.core.security.tokens.base import BaseToken

type TypeJWToken = str
type TypeDictAnyAny = dict[Any, Any]


class BaseJWToken[Token](
    BaseToken[Token],
):
    @classmethod
    def _encrypt_jwtoken(cls, dict_payload: TypeDictAnyAny) -> TypeJWToken:
        return jwt.encode(
            payload=dict_payload,
            key=settings.token.secret_jwt_key,
            algorithm=settings.token.algorithm,
        )

    @classmethod
    def _decrypt_jwtoken(cls, jwtoken: TypeJWToken) -> TypeDictAnyAny:
        return jwt.decode(
            jwt=jwtoken,
            key=settings.token.secret_jwt_key,
            algorithms=[settings.token.algorithm],
        )
