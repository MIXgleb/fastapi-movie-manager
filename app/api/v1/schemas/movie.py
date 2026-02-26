from datetime import (
    datetime,
)
from uuid import (
    UUID,
)

from pydantic import (
    BaseModel as BaseSchema,
)
from pydantic.config import (
    ConfigDict,
)
from pydantic.fields import (
    Field,
)

from app.api.v1.schemas.base import (
    BaseResponse,
)
from app.core.constants import (
    MOVIE_DESCRIPTION_FIELD,
    MOVIE_RATE_FIELD,
    MOVIE_TITLE_FIELD,
    MOVIE_TITLE_PATTERN,
)


class BaseMovieDTO(BaseSchema):
    """Basic scheme of a movie."""

    title: str
    description: str
    rate: float


class MovieInputDTO(BaseMovieDTO):
    """Scheme of getting a movie."""

    title: str = MOVIE_TITLE_FIELD
    description: str = MOVIE_DESCRIPTION_FIELD
    rate: float = MOVIE_RATE_FIELD


class MovieCreateDTO(MovieInputDTO):
    """Scheme of creating a movie."""

    user_id: UUID


class MovieUpdateDTO(BaseMovieDTO):
    """Scheme of updating a movie."""

    title: str = Field(default="", max_length=20, pattern=MOVIE_TITLE_PATTERN)
    description: str = MOVIE_DESCRIPTION_FIELD
    rate: float = Field(default=0, ge=0, le=5)


class MovieOutputDTO(BaseMovieDTO):
    """Scheme of returning a movie."""

    id: int | UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MovieFilterDTO(BaseSchema):
    """Scheme of filtering a movie."""

    limit: int = Field(default=10, le=100, ge=1)
    offset: int = Field(default=0, ge=0)
    sort_by: str = Field(default="id", validation_alias="sort-by")
    rate_from: float = Field(default=0, validation_alias="rate-from")
    rate_to: float = Field(default=5, validation_alias="rate-to")
    title_contains: str | None = Field(default=None, validation_alias="title-contains")

    model_config = ConfigDict(populate_by_name=True)


class ResponseUpdateMovie(BaseResponse):
    """Response scheme for updating a movie."""

    message: str = "Movie has been updated successfully."
    movie: MovieOutputDTO


class ResponseDeleteMovie(BaseResponse):
    """Response scheme for deleting a movie."""

    message: str = "Movie has been removed successfully."
    movie: MovieOutputDTO
