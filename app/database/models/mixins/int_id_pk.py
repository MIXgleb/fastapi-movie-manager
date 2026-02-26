from typing import (
    Never,
)

from sqlalchemy.orm import (
    Mapped,
    declarative_mixin,
    mapped_column,
    validates,
)

import app.core.exceptions as exc


@declarative_mixin
class IntIDMixin:
    """
    Id mixin.

    Columns:
        id: int
    """

    id: Mapped[int] = mapped_column(primary_key=True)

    @validates("id")
    def validate_id_field(
        self,
        field: str,
        _: int,
    ) -> Never:
        raise exc.ImmutableValueError(field)
