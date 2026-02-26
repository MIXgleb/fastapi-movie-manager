from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)
from sqlalchemy.schema import (
    MetaData,
)

from app.core import (
    settings,
)


class BaseModel(DeclarativeBase):
    """Basic database model."""

    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """
        Get the tablename from the classname.

        Returns
        -------
        str
            tablename
        """
        return f"{cls.__name__.lower().removesuffix('model')}s"
