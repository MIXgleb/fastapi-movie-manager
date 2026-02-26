from pydantic import (
    BaseModel as BaseSchema,
)


class BaseResponse(BaseSchema):
    """Basic response schema."""

    message: str
