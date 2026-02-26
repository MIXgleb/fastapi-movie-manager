from typing import (
    final,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import (
    Enum,
    String,
)

from app.database.models.base import (
    BaseModel,
)
from app.database.models.mixins import (
    CreatedAtMixin,
    UpdatedAtMixin,
    UUIDMixin,
)
from app.domains import (
    UserRole,
)


@final
class UserModel(
    UUIDMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    BaseModel,
):
    """
    User database model.

    Columns:
        id: UUID
        created_at: datetime
        updated_at: datetime
        username: str (15)
        hashed_password: str (100)
        role: UserRole
    """

    username: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
        server_default=UserRole.GUEST,
        default=UserRole.GUEST,
    )
    movies = relationship(
        argument="MovieModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )
