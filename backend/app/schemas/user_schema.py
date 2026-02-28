# backend/app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# ----------- Base -----------

class UserBase(BaseModel):
    email: EmailStr


# ----------- Create -----------

class UserCreate(UserBase):
    password: str = Field(min_length=6)


# ----------- Login -----------

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ----------- Response -----------

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ----------- JWT Token -----------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"