from datetime import UTC, datetime
from typing import Never

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.exceptions import ImmutableValueError


def get_current_dt() -> datetime:
    """Get the current UTC datetime.

    Returns
    -------
    datetime
        datetime without timezone
    """
    dt = datetime.now(UTC)
    return dt.replace(microsecond=0, tzinfo=None)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
    )

    @validates("created_at")
    def validate_created_at_field(
        self,
        field: str,
        _: int,
    ) -> Never:
        raise ImmutableValueError(field)


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
        onupdate=get_current_dt,
    )

    @validates("updated_at")
    def validate_updated_at_field(
        self,
        field: str,
        _: int,
    ) -> Never:
        raise ImmutableValueError(field)
