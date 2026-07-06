from pydantic import BaseModel
from datetime import datetime
from typing import List


class ProductBase(BaseModel):
    name: str
    description: str
    cost: float
    pictures: List[str]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    cost: float | None = None
    pictures: List[str] | None = None


class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True