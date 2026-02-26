from datetime import (
    timedelta,
)
from functools import (
    cached_property,
)

from pydantic import (
    BaseModel as BaseSchema,
)
from pydantic.fields import (
    computed_field,
)
from pydantic.types import (
    Secret,
    SecretStr,
)

type SecretInt = Secret[int]
type SecretTTL = Secret[timedelta]


class AuthTokenConfig(BaseSchema):
    """Security token configuration."""

    access_token_ttl: SecretTTL = Secret(timedelta(hours=12))
    refresh_token_ttl: SecretTTL = Secret(timedelta(days=7))
    secret_jwt_key: SecretStr
    secret_fernet_key: SecretStr
    algorithm: SecretStr

    @computed_field
    @cached_property
    def access_token_ttl_seconds(self) -> SecretInt:
        """Access token lifetime in seconds."""
        ttl_seconds = self.access_token_ttl.get_secret_value().total_seconds()
        return Secret(int(ttl_seconds))

    @computed_field
    @cached_property
    def refresh_token_ttl_seconds(self) -> SecretInt:
        """Refresh token lifetime in seconds."""
        ttl_seconds = self.refresh_token_ttl.get_secret_value().total_seconds()
        return Secret(int(ttl_seconds))
