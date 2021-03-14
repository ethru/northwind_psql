from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, LargeBinary, String, Table

from app.api import metadata

categories = Table(
    'categories',
    metadata,
    Column('category_id', Integer, primary_key=True),
    Column('category_name', String),
    Column('description', String),
    Column('picture', LargeBinary)
)


class CategoryIn(BaseModel):
    category_name: str
    description: str
    picture: bytes


class CategoryOut(CategoryIn):
    category_id: int


class CategoryUpdate(CategoryOut):
    category_name: Optional[str] = None
    description: Optional[str] = None
    picture: Optional[bytes] = None
