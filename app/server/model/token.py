from pydantic import BaseModel, Field
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    user_id: str = Field(..., alias='_id')
    username: str
    email: Union[str, None] = None
    role: str
    full_name: Union[str, None] = None
    isVerified: Union[bool, None] = None
    isDisabled: Union[bool, None] = None
    isDeleted: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str
