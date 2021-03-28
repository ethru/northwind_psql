import base64
from functools import wraps
import imghdr
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

from app.api import db
from app.api.auth import authorize
from app.api.models import CategoryIn, CategoryOut, CategoryUpdate

categories = APIRouter()


def raise_404_if_none(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if not result:
            raise HTTPException(status_code=404, detail='Category not found.')
        return result

    return wrapper


@categories.get('/all', response_model=List[CategoryOut])
async def get_all():
    """Return all categories stored in database."""
    return await db.get_categories()


@categories.get('/{category_id}', response_model=CategoryOut)
@raise_404_if_none
async def get_by_id(category_id: int):
    """Return category with set id."""
    return await db.get_category(category_id)


@categories.post('/new', response_model=CategoryOut, status_code=201, dependencies=[Depends(authorize)])
async def create(payload: CategoryIn):
    """Create new category from send data."""
    category_id = await db.add_category(payload)
    return CategoryOut(**payload.dict(), category_id=category_id)


@categories.post('/update/img/{category_id}', dependencies=[Depends(authorize)])
async def upload_file(category_id: int, file: UploadFile = File(...)):
    """Update category with set id by chosen image."""
    if not imghdr.what(file.file):
        raise HTTPException(status_code=415, detail='Wrong image format.')
    image = base64.encodebytes(file.file.read()).decode()
    return await update(CategoryUpdate(category_id=category_id, picture=image))


@categories.put('/update', response_model=CategoryOut, dependencies=[Depends(authorize)])
@raise_404_if_none
async def update(payload: CategoryUpdate):
    """Update category with set id by sent payload."""
    return await db.update(payload.dict(exclude_unset=True))


@categories.delete('/del/{category_id}', response_model=CategoryOut, dependencies=[Depends(authorize)])
async def delete(category_id: int):
    """Delete category with set id."""
    return await db.delete(category_id)
