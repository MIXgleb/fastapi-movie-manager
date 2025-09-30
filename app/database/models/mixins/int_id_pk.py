from typing import Never

from sqlalchemy.orm import Mapped, mapped_column, validates


class IntIdPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)

    @validates("id")
    def validate_id_field(self, field: str, _: int) -> Never:
        exc_msg = f"Field {field!r} is immutable and cannot be modified."
        raise ValueError(exc_msg)
