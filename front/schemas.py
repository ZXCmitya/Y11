from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    password: str
    email: str


class UserAuth(BaseModel):
    username: Optional[str]
    password: Optional[str]
