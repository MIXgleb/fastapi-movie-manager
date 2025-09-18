from typing import final

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.database.models.base import Base
from app.database.models.mixins.created_at import CreatedAtMixin
from app.database.models.mixins.int_id_pk import IntIdPkMixin
from app.schemas import USER_ROLES


@final
class User(IntIdPkMixin, CreatedAtMixin, Base):
    username: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[USER_ROLES] = mapped_column(String(10), nullable=False)
    movies = relationship("Movie", back_populates="user", cascade="all, delete-orphan")
