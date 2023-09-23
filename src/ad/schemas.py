from datetime import datetime

from pydantic import BaseModel


class AdTypeCreate(BaseModel):
    id: int
    name: str


class AdCategoryCreate(BaseModel):
    id: int
    name: str


class AdCreate(BaseModel):
    id: int
    name: str
    type_id: int
    category_id: int
    description: str
    price: str
    created_at: datetime
    updated_at: datetime
    user_id: int
