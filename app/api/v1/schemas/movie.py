from pydantic import BaseModel

from app.schemas import MovieOutput


class MessageDeleteMovieReturn(BaseModel):
    message: str = "Movie has been removed successfully."
    movie: MovieOutput


class MessageUpdateMovieReturn(BaseModel):
    message: str = "Movie has been updated successfully."
    movie: MovieOutput
