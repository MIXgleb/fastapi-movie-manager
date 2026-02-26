from typing import (
    final,
)
from uuid import (
    UUID,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.schema import (
    CheckConstraint,
    ForeignKey,
)
from sqlalchemy.types import (
    Numeric,
    String,
)

from app.database.models.base import (
    BaseModel,
)
from app.database.models.mixins import (
    CreatedAtMixin,
    IntIDMixin,
    UpdatedAtMixin,
)


@final
class MovieModel(
    IntIDMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    BaseModel,
):
    """
    Movie database model.

    Columns:
        id: int
        created_at: datetime
        updated_at: datetime
        title: str (50)
        description: str (100)
        rate: float (0.0-5.0)
        user_id: UUID
    """

    title: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    rate: Mapped[float] = mapped_column(
        Numeric(2, 1),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )
    user = relationship(
        argument="UserModel",
        back_populates="movies",
    )

    __table_args__ = (
        CheckConstraint(
            sqltext="rate >= 0 AND rate <= 5.0",
            name="check_rate_range",
        ),
    )
