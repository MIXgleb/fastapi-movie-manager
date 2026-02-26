from datetime import (
    UTC,
    datetime,
)
from typing import (
    Never,
)

from sqlalchemy.orm import (
    Mapped,
    declarative_mixin,
    mapped_column,
    validates,
)
from sqlalchemy.sql.expression import (
    func,
)

import app.core.exceptions as exc


def get_current_dt() -> datetime:
    """
    Get the current UTC datetime.

    Returns
    -------
    datetime
        datetime without timezone
    """
    return datetime.now(UTC).replace(microsecond=0, tzinfo=None)


@declarative_mixin
class CreatedAtMixin:
    """
    CreatedAt mixin.

    Columns:
        created_at: datetime
    """

    created_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
    )

    @validates("created_at")
    def validate_created_at_field(
        self,
        field: str,
        _: datetime,
    ) -> Never:
        raise exc.ImmutableValueError(field)


@declarative_mixin
class UpdatedAtMixin:
    """
    UpdatedAt mixin.

    Columns:
        updated_at: datetime
    """

    updated_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
        onupdate=get_current_dt,
    )

    @validates("updated_at")
    def validate_updated_at_field(
        self,
        field: str,
        _: datetime,
    ) -> Never:
        raise exc.ImmutableValueError(field)
