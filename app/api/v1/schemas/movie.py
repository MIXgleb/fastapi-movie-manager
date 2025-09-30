from datetime import datetime
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

MOVIE_TITLE_PATTERN: Final[str] = r"^[\w\s\d\.,!?@#%&*()_+\-=\[\]{}|;:\"<>`]+$"
MOVIE_DESCRIPTION_PATTERN: Final[str] = r"^[\w\s\d\.,!?@#%&*()_+\-=\[\]{}|;:\"<>`]+$"
TITLE_INPUT_FIELD: Final = Field(max_length=30, pattern=MOVIE_TITLE_PATTERN)
DESCRIPTION_INPUT_FIELD: Final = Field(
    default="",
    max_length=100,
    pattern=MOVIE_DESCRIPTION_PATTERN,
)
RATE_INPUT_FIELD: Final = Field(ge=0, le=5)


class MovieBaseModel(BaseModel):
    title: str
    description: str
    rate: float


class MovieInputDTO(MovieBaseModel):
    title: str = TITLE_INPUT_FIELD
    description: str = DESCRIPTION_INPUT_FIELD
    rate: float = RATE_INPUT_FIELD


class MovieCreateDTO(MovieInputDTO):
    user_id: int


class MovieUpdateDTO(MovieBaseModel):
    title: str = Field(default="", max_length=20, pattern=MOVIE_TITLE_PATTERN)
    description: str = DESCRIPTION_INPUT_FIELD
    rate: float = Field(default=0, ge=0, le=5)


class MovieOutputDTO(MovieBaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MovieFilterDTO(BaseModel):
    limit: int = Field(default=10, le=100, ge=1)
    offset: int = Field(default=0, ge=0)
    sort_by: str = Field(default="id", validation_alias="sort-by")
    rate_from: float = Field(default=0, validation_alias="rate-from")
    rate_to: float = Field(default=5, validation_alias="rate-to")
    title_contains: str | None = Field(default=None, validation_alias="title-contains")

    model_config = ConfigDict(populate_by_name=True)


class UpdateMovieResponse(BaseModel):
    message: str = "Movie has been updated successfully."
    movie: MovieOutputDTO


class DeleteMovieResponse(BaseModel):
    message: str = "Movie has been removed successfully."
    movie: MovieOutputDTO
