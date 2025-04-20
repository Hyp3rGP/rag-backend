from pydantic import BaseModel, EmailStr, Field
from typing import Optional



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
