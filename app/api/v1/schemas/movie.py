from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import (
    MOVIE_DESCRIPTION_INPUT_FIELD,
    MOVIE_RATE_INPUT_FIELD,
    MOVIE_TITLE_INPUT_FIELD,
    MOVIE_TITLE_PATTERN,
)


class MovieBaseModel(BaseModel):
    title: str
    description: str
    rate: float


class MovieInputDTO(MovieBaseModel):
    title: str = MOVIE_TITLE_INPUT_FIELD
    description: str = MOVIE_DESCRIPTION_INPUT_FIELD
    rate: float = MOVIE_RATE_INPUT_FIELD


class MovieCreateDTO(MovieInputDTO):
    user_id: int


class MovieUpdateDTO(MovieBaseModel):
    title: str = Field(default="", max_length=20, pattern=MOVIE_TITLE_PATTERN)
    description: str = MOVIE_DESCRIPTION_INPUT_FIELD
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
