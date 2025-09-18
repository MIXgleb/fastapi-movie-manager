from pydantic import BaseModel, ConfigDict, Field


class MovieBase(BaseModel):
    title: str
    description: str
    rate: float


class MovieInput(MovieBase):
    title: str = Field(max_length=20)
    rate: float = Field(ge=0, le=5)
    description: str = Field(default="none", max_length=100)


class MovieCreate(MovieInput):
    user_id: int


class MovieUpdate(MovieBase):
    title: str = Field(default="", max_length=20)
    rate: float = Field(default=0, ge=0, le=5)
    description: str = Field(default="", max_length=100)


class MovieOutput(MovieBase):
    id: int


class MovieFilters(MovieBase):
    limit: int = Field(default=10, le=100, ge=1)
    offset: int = Field(default=0, ge=0)
    sort_by: str = Field(default="id", validation_alias="sort-by")
    rate_from: float = Field(default=0, validation_alias="rate-from")
    rate_to: float = Field(default=5, validation_alias="rate-to")
    title_contains: str | None = Field(default=None, validation_alias="title-contains")

    model_config = ConfigDict(populate_by_name=True)
