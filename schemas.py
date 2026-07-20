from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# PRODUCT SCHEMAS

class ProductBase(BaseModel):
    name: str
    description: str
    cost: float
    pictures: List[str]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    pictures: Optional[List[str]] = None


class ProductOut(ProductBase):
    id: int
    admin_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# USER SCHEMAS

class UserBase(BaseModel):
    full_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)


# PASSWORD SCHEMAS

class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str


# TOKEN SCHEMA

class Token(BaseModel):
    access_token: str
    token_type: str