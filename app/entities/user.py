from typing import List

from pydantic import BaseModel, EmailStr
from .role import Role


class UserBase(BaseModel):
    email: EmailStr
    roles: List[Role] = []
    full_name: str
    username: str


# password is only on the schema when creating user
# it should never appear in other schemas.
class UserInput(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    hashed_password: str

    class Config:
        orm_mode = True
