from typing import (
    Annotated,
    final,
    override,
)
from uuid import (
    UUID,
)

from fastapi import (
    Depends,
    Request,
    Response,
)

import app.core.exceptions as exc
from app.core.config import (
    AuthTokenConfig,
)
from app.domains import (
    UserRole,
)
from app.security.auth import (
    GUEST_PAYLOAD,
    AuthAccessJWT,
    AuthJWTReadDTO,
    AuthJWTRepository,
    AuthRefreshJWT,
    Payload,
    TokenKey,
)
from app.security.auth_managers.base import (
    BaseAuthManager,
)


class BaseAuthJWTManager(
    BaseAuthManager[
        UUID,
        Payload,
        AuthAccessJWT | AuthRefreshJWT,
        AuthJWTReadDTO,
        AuthTokenConfig,
    ],
):
    """Basic abstract auth jwt manager class."""

    @final
    @classmethod
    def _get_payload_from_state(
        cls,
        request: Request,
    ) -> Payload:
        payload: Payload = request.state.payload
        return payload

    @final
    @classmethod
    def _save_payload_to_state(
        cls,
        request: Request,
        new_payload: Payload,
    ) -> None:
        request.state.payload = new_payload

    @final
    @classmethod
    def _delete_payload_from_state(
        cls,
        request: Request,
    ) -> None:
        request.state.payload = GUEST_PAYLOAD

    @final
    @classmethod
    def _get_tokens_from_state(
        cls,
        request: Request,
    ) -> AuthJWTReadDTO:
        tokens: AuthJWTReadDTO = request.state.tokens
        return tokens

    @final
    @classmethod
    def _save_tokens_to_state(
        cls,
        request: Request,
        new_tokens: AuthJWTReadDTO,
    ) -> None:
        request.state.tokens = new_tokens

    @final
    @classmethod
    def _delete_tokens_from_state(
        cls,
        request: Request,
    ) -> None:
        request.state.tokens = AuthJWTReadDTO()


@final
class AuthJWTManager(BaseAuthJWTManager):
    """Auth JWT manager."""

    _repo = AuthJWTRepository()

    @override
    async def store_payload(
        self,
        tokens: AuthJWTReadDTO,
        request: Request,
    ) -> None:
        if tokens.access_token is None and tokens.refresh_token is None:
            self._save_payload_to_state(
                request=request,
                new_payload=GUEST_PAYLOAD,
            )
            return

        if tokens.access_token is None or tokens.refresh_token is None:
            raise exc.InvalidTokenError

        payload = await self._repo.read_token(
            token=AuthAccessJWT(
                token_config=self.auth_config,
                token=tokens.access_token,
            ),
        )
        self._save_payload_to_state(
            request=request,
            new_payload=payload,
        )

    @override
    async def store_tokens(
        self,
        tokens: AuthJWTReadDTO,
        request: Request,
    ) -> None:
        self._save_tokens_to_state(
            request=request,
            new_tokens=tokens,
        )

    @override
    async def check_admin_rights(
        self,
        request: Request,
    ) -> None:
        payload = self._get_payload_from_state(request)

        if payload.user_role is not UserRole.ADMIN:
            raise exc.UserPermissionError

    @override
    async def validate_tokens(
        self,
        request: Request,
    ) -> AuthJWTReadDTO:
        tokens = AuthJWTReadDTO(
            access_token=request.cookies.get(TokenKey.ACCESS_TOKEN),
            refresh_token=request.cookies.get(TokenKey.REFRESH_TOKEN),
        )

        if tokens.access_token is None and tokens.refresh_token is None:
            return tokens

        if tokens.refresh_token is None:
            raise exc.InvalidTokenError

        if tokens.access_token is None:
            access_token = AuthAccessJWT(
                token_config=self.auth_config,
            )
            refresh_token = AuthRefreshJWT(
                token_config=self.auth_config,
                token=tokens.refresh_token,
            )
            payload = await self._repo.read_token(refresh_token)

            updated_tokens = await self._repo.create_tokens(
                access_token=access_token,
                refresh_token=refresh_token,
                payload=payload,
            )
            return AuthJWTReadDTO.model_validate(
                updated_tokens,
                from_attributes=True,
            )

        return tokens

    @override
    async def generate_tokens(
        self,
        payload: Payload,
        request: Request,
    ) -> None:
        created_tokens = await self._repo.create_tokens(
            access_token=AuthAccessJWT(
                token_config=self.auth_config,
            ),
            refresh_token=AuthRefreshJWT(
                token_config=self.auth_config,
            ),
            payload=payload,
        )
        tokens = AuthJWTReadDTO.model_validate(
            created_tokens,
            from_attributes=True,
        )
        self._save_tokens_to_state(
            request=request,
            new_tokens=tokens,
        )
        self._save_payload_to_state(
            request=request,
            new_payload=payload,
        )

    @override
    async def update_tokens(
        self,
        updated_payload: Payload,
        request: Request,
        response: Response,
    ) -> None:
        payload = self._get_payload_from_state(request)

        if await self._repo.is_user_initiator(
            payload_initiator=payload,
            key=updated_payload.user_id,
        ):
            updated_base_tokens = await self._repo.create_tokens(
                access_token=AuthAccessJWT(
                    token_config=self.auth_config,
                ),
                refresh_token=AuthRefreshJWT(
                    token_config=self.auth_config,
                ),
                payload=updated_payload,
            )
            updated_tokens = AuthJWTReadDTO.model_validate(
                updated_base_tokens,
                from_attributes=True,
            )
            self._save_tokens_to_state(
                request=request,
                new_tokens=updated_tokens,
            )
            self._save_payload_to_state(
                request=request,
                new_payload=updated_payload,
            )
        else:
            await self._repo.delete_tokens(
                access_token=AuthAccessJWT(
                    token_config=self.auth_config,
                ),
                refresh_token=AuthRefreshJWT(
                    token_config=self.auth_config,
                ),
                response=response,
                key=updated_payload.user_id,
            )

    @override
    async def clear_tokens(
        self,
        request: Request,
        response: Response,
        user_id: UUID | None = None,
    ) -> None:
        payload = self._get_payload_from_state(request)

        if user_id is None or await self._repo.is_user_initiator(
            payload_initiator=payload,
            key=user_id,
        ):
            self._delete_tokens_from_state(request)
            self._delete_payload_from_state(request)
        else:
            await self._repo.delete_tokens(
                access_token=AuthAccessJWT(
                    token_config=self.auth_config,
                ),
                refresh_token=AuthRefreshJWT(
                    token_config=self.auth_config,
                ),
                response=response,
                key=user_id,
            )

    @override
    async def save_tokens(
        self,
        request: Request,
        response: Response,
    ) -> None:
        old_tokens = AuthJWTReadDTO(
            access_token=request.cookies.get(TokenKey.ACCESS_TOKEN),
            refresh_token=request.cookies.get(TokenKey.REFRESH_TOKEN),
        )
        cur_tokens = self._get_tokens_from_state(request)
        payload = self._get_payload_from_state(request)

        if old_tokens != cur_tokens:
            await self._repo.delete_tokens(
                access_token=AuthAccessJWT(
                    token_config=self.auth_config,
                    token=old_tokens.access_token,
                ),
                refresh_token=AuthRefreshJWT(
                    token_config=self.auth_config,
                    token=old_tokens.refresh_token,
                ),
                response=response,
            )

            if cur_tokens.access_token is not None and cur_tokens.refresh_token is not None:
                await self._repo.save_tokens(
                    access_token=AuthAccessJWT(
                        token_config=self.auth_config,
                        token=cur_tokens.access_token,
                    ),
                    refresh_token=AuthRefreshJWT(
                        token_config=self.auth_config,
                        token=cur_tokens.refresh_token,
                    ),
                    response=response,
                    payload=Payload.model_validate(payload),
                )

    @classmethod
    @override
    async def payload_getter(
        cls,
        request: Request,
    ) -> Payload:
        return cls._get_payload_from_state(request)


PayloadDep = Annotated[
    Payload,
    Depends(AuthJWTManager.payload_getter),
]
