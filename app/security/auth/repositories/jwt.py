from typing import (
    final,
    override,
)
from uuid import (
    UUID,
)

from app.core.config import (
    AuthTokenConfig,
)
from app.security.auth.repositories.base import (
    BaseSyncAsyncAuthTokenRepository,
)
from app.security.auth.schemas import (
    Payload,
)


@final
class AuthJWTRepository(
    BaseSyncAsyncAuthTokenRepository[
        int | UUID,
        Payload,
        AuthTokenConfig,
    ],
):
    """Auth JWT repository."""

    @classmethod
    @override
    async def is_user_initiator(
        cls,
        payload_initiator: Payload,
        key: int | UUID,
    ) -> bool:
        return key == payload_initiator.user_id
