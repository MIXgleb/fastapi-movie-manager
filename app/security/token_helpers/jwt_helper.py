from typing import Annotated, final, override

from fastapi import Depends, Request, Response

import app.core.exceptions as exc
from app.security.token_helpers.base import BaseTokenHelper
from app.security.token_repositories import JWTokenRepository
from app.security.token_schemas import (
    JWTokenReadDTO,
    Payload,
    TokenKey,
    UserRole,
)
from app.security.tokens import AccessJWToken, RefreshJWToken

_guest_payload = Payload(user_id=0, user_role=UserRole.guest)


class BaseJWTokenHelper(
    BaseTokenHelper[
        int,
        Payload,
        AccessJWToken | RefreshJWToken,
        JWTokenReadDTO,
    ],
):
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
        request.state.payload = _guest_payload

    @final
    @classmethod
    def _get_tokens_from_state(
        cls,
        request: Request,
    ) -> JWTokenReadDTO:
        tokens: JWTokenReadDTO = request.state.tokens
        return tokens

    @final
    @classmethod
    def _save_tokens_to_state(
        cls,
        request: Request,
        new_tokens: JWTokenReadDTO,
    ) -> None:
        request.state.tokens = new_tokens

    @final
    @classmethod
    def _delete_tokens_from_state(
        cls,
        request: Request,
    ) -> None:
        request.state.tokens = JWTokenReadDTO()


@final
class JWTokenHelper(BaseJWTokenHelper):
    tokens = JWTokenRepository()

    @classmethod
    @override
    async def store_payload(
        cls,
        tokens: JWTokenReadDTO,
        request: Request,
    ) -> None:
        if tokens.access_token is None and tokens.refresh_token is None:
            cls._save_payload_to_state(request, _guest_payload)
            return

        if tokens.access_token is None or tokens.refresh_token is None:
            raise exc.InvalidTokenError

        payload = await cls.tokens.read_token(
            token=AccessJWToken(tokens.access_token),
        )
        cls._save_payload_to_state(request, payload)

    @classmethod
    @override
    async def store_tokens(
        cls,
        tokens: JWTokenReadDTO,
        request: Request,
    ) -> None:
        cls._save_tokens_to_state(request, tokens)

    @classmethod
    @override
    async def check_admin_rights(
        cls,
        request: Request,
    ) -> None:
        payload = cls._get_payload_from_state(request)

        if payload.user_role != UserRole.admin:
            raise exc.UserPermissionError

    @classmethod
    @override
    async def validate_tokens(
        cls,
        request: Request,
    ) -> JWTokenReadDTO:
        tokens = JWTokenReadDTO(
            access_token=request.cookies.get(TokenKey.access_token),
            refresh_token=request.cookies.get(TokenKey.refresh_token),
        )

        if tokens.access_token is None and tokens.refresh_token is None:
            return tokens

        if tokens.refresh_token is None:
            raise exc.InvalidTokenError

        if tokens.access_token is None:
            access_token = AccessJWToken()
            refresh_token = RefreshJWToken(tokens.refresh_token)
            payload = await cls.tokens.read_token(refresh_token)

            updated_tokens = await cls.tokens.create_tokens(
                access_token=access_token,
                refresh_token=refresh_token,
                payload=payload,
            )
            return JWTokenReadDTO.model_validate(updated_tokens, from_attributes=True)

        return tokens

    @classmethod
    @override
    async def generate_tokens(
        cls,
        payload: Payload,
        request: Request,
    ) -> None:
        created_tokens = await cls.tokens.create_tokens(
            access_token=AccessJWToken(),
            refresh_token=RefreshJWToken(),
            payload=payload,
        )
        tokens = JWTokenReadDTO.model_validate(
            created_tokens,
            from_attributes=True,
        )
        cls._save_tokens_to_state(request, tokens)
        cls._save_payload_to_state(request, payload)

    @classmethod
    @override
    async def update_tokens(
        cls,
        updated_payload: Payload,
        request: Request,
        response: Response,
    ) -> None:
        payload = cls._get_payload_from_state(request)

        if await cls.tokens.is_user_initiator(payload, updated_payload.user_id):
            updated_base_tokens = await cls.tokens.create_tokens(
                access_token=AccessJWToken(),
                refresh_token=RefreshJWToken(),
                payload=updated_payload,
            )
            updated_tokens = JWTokenReadDTO.model_validate(
                updated_base_tokens,
                from_attributes=True,
            )
            cls._save_tokens_to_state(request, updated_tokens)
            cls._save_payload_to_state(request, updated_payload)
        else:
            await cls.tokens.delete_tokens(
                access_token=AccessJWToken(),
                refresh_token=RefreshJWToken(),
                response=response,
                key=updated_payload.user_id,
            )

    @classmethod
    @override
    async def clear_tokens(
        cls,
        request: Request,
        response: Response,
        user_id: int | None = None,
    ) -> None:
        payload = cls._get_payload_from_state(request)

        if user_id is None or await cls.tokens.is_user_initiator(payload, user_id):
            cls._delete_tokens_from_state(request)
            cls._delete_payload_from_state(request)
        else:
            await cls.tokens.delete_tokens(
                access_token=AccessJWToken(),
                refresh_token=RefreshJWToken(),
                response=response,
                key=user_id,
            )

    @classmethod
    @override
    async def save_tokens(
        cls,
        request: Request,
        response: Response,
    ) -> None:
        old_tokens = JWTokenReadDTO(
            access_token=request.cookies.get(TokenKey.access_token),
            refresh_token=request.cookies.get(TokenKey.refresh_token),
        )
        cur_tokens = cls._get_tokens_from_state(request)
        payload = cls._get_payload_from_state(request)

        if old_tokens != cur_tokens:
            await cls.tokens.delete_tokens(
                access_token=AccessJWToken(old_tokens.access_token),
                refresh_token=RefreshJWToken(old_tokens.refresh_token),
                response=response,
            )

            if cur_tokens.access_token is not None and cur_tokens.refresh_token is not None:
                await cls.tokens.save_tokens(
                    access_token=AccessJWToken(cur_tokens.access_token),
                    refresh_token=RefreshJWToken(cur_tokens.refresh_token),
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


PayloadFromToken = Annotated[
    Payload,
    Depends(JWTokenHelper.payload_getter),
]
