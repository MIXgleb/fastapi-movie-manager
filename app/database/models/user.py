from typing import final

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.database.models.base import Base
from app.database.models.mixins import (
    CreatedAtMixin,
    IntIdPkMixin,
    UpdatedAtMixin,
)
from app.domains import UserRoleType


@final
class User(IntIdPkMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    username: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRoleType] = mapped_column(String(10), nullable=False)
    movies = relationship(
        argument="Movie",
        back_populates="user",
        cascade="all, delete-orphan",
    )
