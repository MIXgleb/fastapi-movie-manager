import uuid
from typing import final

from sqlalchemy import UUID, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.database.models.base import Base
from app.database.models.mixins.created_at import CreatedAtMixin


@final
class Movie(CreatedAtMixin, Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v7(),
        primary_key=True,
    )
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    rate: Mapped[float] = mapped_column(Float(), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="movies")
