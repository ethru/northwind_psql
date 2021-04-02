from fastapi import APIRouter, Depends
from typing import List

from app.api import db
from app.api.auth import authorize
from app.api.models import Date, ProductPopular, ProductReorder

reports = APIRouter()


@reports.post('/products/popularity', response_model=List[ProductPopular], dependencies=[Depends(authorize)])
async def get_products_sales(payload: Date):
    """Return total number of each sold product in set period of time."""
    return await db.get_products_by_popularity(**payload.dict())


@reports.get('/products/reorder', response_model=List[ProductReorder], dependencies=[Depends(authorize)])
async def get_products_to_reorder():
    """Return report about products to reorder."""
    return await db.get_products_to_reorder()
