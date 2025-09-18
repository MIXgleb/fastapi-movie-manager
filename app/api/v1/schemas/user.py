from pydantic import BaseModel

from app.schemas import UserOutput


class MessageDeleteUserReturn(BaseModel):
    message: str = "User has been removed successfully."
    user: UserOutput
