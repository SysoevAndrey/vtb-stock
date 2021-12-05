from pydantic import BaseModel


class NotFoundError(BaseModel):
    message: str
