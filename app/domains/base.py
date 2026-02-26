from dataclasses import (
    asdict,
    dataclass,
    fields,
)
from typing import (
    Any,
    ClassVar,
    Protocol,
    Self,
    assert_never,
    final,
    runtime_checkable,
)

from pydantic import (
    BaseModel as BaseSchema,
)
from sqlalchemy.orm import (
    DeclarativeBase,
)

from app.core.typing_ import (
    KwargsType,
)


@runtime_checkable
class DataclassType(Protocol):
    """Dataclass protocol."""

    __dataclass_fields__: ClassVar[dict[str, Any]]


@dataclass(frozen=True)
class BaseDataclass:
    """Basic abstract dataclass."""

    @final
    def as_dict(
        self,
        *,
        exclude_none: bool = False,
    ) -> dict[Any, Any]:
        """
        Convert to Dictionary.

        Parameters
        ----------
        exclude_none : bool, optional
            exclude 'None' values, by default False

        Returns
        -------
        dict[Any, Any]
            parameters as dictionary
        """
        if exclude_none:
            return {k: v for k, v in asdict(self).items() if v is not None}
        return asdict(self)

    @final
    @classmethod
    def from_object(
        cls,
        object_: dict[Any, Any] | DeclarativeBase | DataclassType | BaseSchema,
        /,
        *,
        none_if_key_not_found: bool = False,
        **kwargs: KwargsType,
    ) -> Self:
        """
        Create a dataclass from the specified object.

        Parameters
        ----------
        object_ : dict[Any, Any] | DeclarativeBase | DataclassType | BaseSchema
            object with parameters

        none_if_key_not_found : bool, optional
            specify an argument as 'None' or raise a KeyError, \
                by default False

        **kwargs : KwargsType
            key arguments to add manually

        Returns
        -------
        Self
            dataclass instance

        Raises
        ------
        KeyError
            key not found
        """
        result_dict: dict[Any, Any] = {}

        for param in fields(cls):
            name = param.name

            match object_:
                case dict():
                    if name not in object_:
                        if not none_if_key_not_found:
                            break
                        result_dict[name] = None
                    else:
                        result_dict[name] = object_[name]

                case DeclarativeBase() | BaseSchema() | DataclassType():
                    if not hasattr(object_, name):
                        if not none_if_key_not_found:
                            break
                        result_dict[name] = None
                    else:
                        result_dict[name] = getattr(object_, name)

                case _:
                    assert_never(object_)
        else:
            result_dict.update(kwargs)
            return cls(**result_dict)

        exc_msg = f"Key {name!r} not found in dictionary"
        raise KeyError(exc_msg)
