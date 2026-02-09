from typing import (
    Never,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    validates,
)

from app.core.exceptions import (
    ImmutableValueError,
)


class IntIdPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)

    @validates("id")
    def validate_id_field(
        self,
        field: str,
        _: int,
    ) -> Never:
        raise ImmutableValueError(field)
