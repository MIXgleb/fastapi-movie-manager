from typing import (
    final,
)

from sqlalchemy import (
    Float,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import (
    String,
)

from app.database.models.base import (
    Base,
)
from app.database.models.mixins import (
    CreatedAtMixin,
    IntIdPkMixin,
    UpdatedAtMixin,
)


@final
class Movie(
    IntIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    title: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    rate: Mapped[float] = mapped_column(
        Float(),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    user = relationship(
        argument="User",
        back_populates="movies",
    )
