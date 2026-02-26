from datetime import (
    UTC,
    datetime,
)
from enum import (
    StrEnum,
)
from functools import (
    cached_property,
)
from typing import (
    Any,
    Final,
    Self,
    assert_never,
)
from uuid import (
    UUID,
)

from pydantic import (
    BaseModel as BaseSchema,
)
from pydantic.config import (
    ConfigDict,
)
from pydantic.fields import (
    computed_field,
)
from pydantic.functional_serializers import (
    field_serializer,
)
from pydantic.functional_validators import (
    model_validator,
)

from app.core import (
    settings,
)
from app.domains import (
    UserRole,
)

ZERO_IDS: Final[set[Any]] = {0, UUID(int=0)}


class TokenKey(StrEnum):
    """Token keys."""

    ACCESS_TOKEN = "access_token"  # noqa: S105
    REFRESH_TOKEN = "refresh_token"  # noqa: S105


class BaseAuthTokenDTO(BaseSchema):
    """Basic scheme of a token."""

    access_token: Any
    refresh_token: Any


class AuthJWTReadDTO(BaseAuthTokenDTO):
    """Scheme of getting a token."""

    access_token: str | None = None
    refresh_token: str | None = None


class BasePayload(BaseSchema):
    """Basic scheme of a payload."""

    user_id: UUID


class Payload(BasePayload):
    """Scheme of a payload."""

    user_role: UserRole

    model_config = ConfigDict(from_attributes=True)


class JWTPayload(Payload):
    """Scheme of a jwt payload."""

    token_type: TokenKey

    @computed_field
    @cached_property
    def exp(self) -> datetime:
        """
        Token expiration time.

        Returns
        -------
        datetime
            expiration time
        """
        match self.token_type.value:
            case "access_token":
                return (
                    datetime.now(UTC) + settings.auth_token.access_token_ttl.get_secret_value()
                )
            case "refresh_token":
                return (
                    datetime.now(UTC)
                    + settings.auth_token.refresh_token_ttl.get_secret_value()
                )
            case _:
                assert_never(self.token_type)

    @model_validator(mode="after")
    def check_user_id(self) -> Self:
        """
        Validate a user's id.

        Returns
        -------
        Self
            payload data

        Raises
        ------
        ValueError
            incorrect user id
        """
        if self.user_id not in ZERO_IDS or self.user_role is UserRole.GUEST:
            return self

        raise ValueError

    @field_serializer("user_id", check_fields=True)
    def serialize_user_id(
        self,
        user_id: UUID,
    ) -> str:
        """
        Automatically serializes the UUID to a string.

        Parameters
        ----------
        user_id : UUID
            user id

        Returns
        -------
        str
            user id in string format
        """
        return str(user_id)


GUEST_PAYLOAD: Final[Payload] = Payload(
    user_id=UUID(int=0),
    user_role=UserRole.GUEST,
)
