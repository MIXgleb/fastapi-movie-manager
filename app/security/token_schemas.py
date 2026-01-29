import functools
from datetime import UTC, datetime
from typing import (
    Any,
    ClassVar,
    Literal,
    Self,
    assert_never,
    final,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
    model_validator,
)

from app.core import settings
from app.domains import TypeUserRole, UserRole

type TypeToken = Literal["access_token", "refresh_token"]


@final
class TokenKey:
    access_token: ClassVar[TypeToken] = "access_token"  # noqa: S105
    refresh_token: ClassVar[TypeToken] = "refresh_token"  # noqa: S105


class TokenBaseModel(BaseModel):
    access_token: Any
    refresh_token: Any


class JWTokenReadDTO(TokenBaseModel):
    access_token: str | None = None
    refresh_token: str | None = None


class Payload(BaseModel):
    user_id: int
    user_role: TypeUserRole

    model_config = ConfigDict(from_attributes=True)


class JWTokenPayload(Payload):
    token_type: TypeToken

    @computed_field
    @functools.cached_property
    def exp(self) -> datetime:
        """Token expiration time.

        Returns
        -------
        datetime
            expiration time
        """
        match self.token_type:
            case "access_token":
                return datetime.now(UTC) + settings.token.access_token_ttl
            case "refresh_token":
                return datetime.now(UTC) + settings.token.refresh_token_ttl
            case _:
                assert_never(self.token_type)

    @model_validator(mode="after")
    def check_user_id(self) -> Self:
        """Validate the user's id.

        Returns
        -------
        Self
            payload data

        Raises
        ------
        ValueError
            incorrect user id
        """
        if self.user_id != 0 or self.user_role == UserRole.guest:
            return self

        raise ValueError
