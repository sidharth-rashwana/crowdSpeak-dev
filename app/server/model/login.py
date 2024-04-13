from pydantic import BaseModel
from fastapi import Body
from typing import Union, Optional, Any
from uuid import uuid1
from pydantic import EmailStr


class SignUp(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: str = "user"


class SignIn(BaseModel):
    email: str
    password: str


class otp(BaseModel):
    email: EmailStr
