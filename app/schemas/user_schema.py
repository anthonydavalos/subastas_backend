from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="john@example.com")

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
