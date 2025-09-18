from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

type USER_ROLES = Literal["guest", "user", "admin"]


class Role:
    guest: USER_ROLES = "guest"
    user: USER_ROLES = "user"
    admin: USER_ROLES = "admin"


class UserBase(BaseModel):
    username: str = Field(max_length=20)


class UserInput(UserBase):
    password: str = Field(max_length=30)


class UserCreate(UserBase):
    hashed_password: str
    role: USER_ROLES


class UserOutput(UserBase):
    id: int
    created_at: datetime
    role: USER_ROLES


class UserFilters(BaseModel):
    limit: int = Field(default=10, le=100, ge=1)
    offset: int = Field(default=0, ge=0)
    sort_by: str = Field(default="id", validation_alias="sort-by")
    username_contains: str | None = Field(default=None, validation_alias="username-contains")
    role: list[USER_ROLES] | None = None

    model_config = ConfigDict(populate_by_name=True)
