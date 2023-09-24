from datetime import datetime

from pydantic import BaseModel


class AdTypeCreate(BaseModel):
    id: int
    name: str


class AdCategoryCreate(BaseModel):
    id: int
    type_id: int
    name: str


class AdCreate(BaseModel):
    name: str
    category_id: int
    description: str
    price: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    user_id: int


class AdComments(BaseModel):
    value: str
    ad_id: int
    user_id: int
    created_at: datetime = datetime.utcnow()
