from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    name: str


class UserAuth(BaseModel):
    username: Optional[str]
    password: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
