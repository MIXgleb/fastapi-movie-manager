from typing import (
    Never,
)
from uuid import (
    UUID,
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


@declarative_mixin
class UUIDMixin:
    """
    UUID mixin.

    Columns:
        id: UUID
    """

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),  # PostgreSQL18: func.uuidv7()
    )

    @validates("id")
    def validate_id_field(
        self,
        field: str,
        _: UUID,
    ) -> Never:
        raise exc.ImmutableValueError(field)
