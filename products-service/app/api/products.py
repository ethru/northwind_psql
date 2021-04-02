from functools import wraps
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.api import db
from app.api.auth import authorize
from app.api.models import ProductIn, ProductOut, ProductUpdate, ProductSearch

products = APIRouter()


def raise_404_if_none(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if not result:
            raise HTTPException(status_code=404, detail='Product not found.')
        return result

    return wrapper


@products.get('/{product_id}', response_model=ProductOut)
@raise_404_if_none
async def get_by_id(product_id: int):
    """Return product with set id."""
    return await db.get_product(product_id)


@products.post('/search', response_model=List[ProductOut])
async def search(payload: ProductSearch):
    """Return products matching payload."""
    return await db.search(payload.dict(exclude_unset=True))


@products.post('/new', response_model=ProductOut, status_code=201, dependencies=[Depends(authorize)])
async def create(payload: ProductIn):
    """Create new product from sent data."""
    product_id = await db.add_product(payload)
    return ProductOut(**payload.dict(), product_id=product_id)


@products.put('/update', response_model=ProductOut, dependencies=[Depends(authorize)])
@raise_404_if_none
async def update(payload: ProductUpdate):
    """Update product with set id by sent payload."""
    return await db.update(payload.dict(exclude_unset=True))


@products.delete('/del/{product_id}', response_model=ProductOut, dependencies=[Depends(authorize)])
@raise_404_if_none
async def delete(product_id: int):
    """Delete product with set id."""
    return await db.delete(product_id)
