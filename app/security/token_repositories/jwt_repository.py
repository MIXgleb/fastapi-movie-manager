from typing import final, override

from app.security.token_repositories.base import BaseSyncAsyncTokenRepository
from app.security.token_schemas import Payload


@final
class JWTokenRepository(
    BaseSyncAsyncTokenRepository[
        int,
        Payload,
    ],
):
    @final
    @classmethod
    @override
    async def is_user_initiator(
        cls,
        payload_initiator: Payload,
        key: int,
    ) -> bool:
        return key == payload_initiator.user_id
