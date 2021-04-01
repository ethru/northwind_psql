from typing import Optional

from pydantic import BaseModel, validator
from sqlalchemy import Column, Integer, ForeignKeyConstraint, String, Table

from app.api import metadata

products = Table(
    'products',
    metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('supplier_id', Integer),
    Column('category_id', Integer),
    Column('quantity_per_unit', String),
    Column('unit_price', Integer),
    Column('units_in_stock', Integer),
    Column('units_on_order', Integer),
    Column('reorder_level', Integer),
    Column('discontinued', Integer),
    ForeignKeyConstraint(['supplier_id'], ['suppliers.supplier_id']),
    ForeignKeyConstraint(['category_id'], ['categories.category_id'])
)


class ProductIn(BaseModel):
    product_name: str
    supplier_id: int
    category_id: int
    quantity_per_unit: str
    unit_price: int
    units_in_stock: int
    units_on_order: int
    reorder_level: int
    discontinued: int

    @validator('supplier_id', 'category_id', 'unit_price', 'units_in_stock', 'units_on_order', 'reorder_level')
    def value_must_be_greater_than_0(cls, number):
        if number >= 0:
            return number
        raise ValueError('must be greater or equal 0')

    @validator('discontinued')
    def discontinued_must_be_0_or_1(cls, number):
        if number == 0 or number == 1:
            return number
        raise ValueError('must be 0 or 1')


class ProductOut(ProductIn):
    product_id: int


class ProductUpdate(ProductOut):
    product_name: Optional[str] = None
    supplier_id: Optional[int] = None
    category_id: Optional[int] = None
    quantity_per_unit: Optional[str] = None
    unit_price: Optional[int] = None
    units_in_stock: Optional[int] = None
    units_on_order: Optional[int] = None
    reorder_level: Optional[int] = None
    discontinued: Optional[int] = None


class ProductSearch(ProductUpdate):
    product_id: Optional[int] = None
