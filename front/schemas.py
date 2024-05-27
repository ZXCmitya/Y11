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


class UserPosts(BaseModel):
    id: Optional[int] = None
    username: str
    content: str
    time_of_upload: str
    id_of_user: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None