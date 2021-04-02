from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import HTTPException
from sqlalchemy.sql import and_, select, text

from app.api import database
from app.api.models import ProductIn, ProductOut, products


async def get_product(product_id: int):
    """Get product with set id from database."""
    query = products.select().where(products.c.product_id == product_id)
    print(query)
    return await database.fetch_one(query=query)


async def search(payload: dict):
    """Get products matching payload from database.

    If there is no payload return all products.
    """
    if payload:
        conditions = [getattr(products.c, k) == v for k, v in payload.items()]
        query = select([text('*')]).where(and_(*conditions))
    else:
        query = products.select()

    print(query)
    return await database.fetch_all(query=query)


async def add_product(payload: ProductIn):
    """Store new product in database."""
    query = products.insert().values(**payload.dict())
    print(query)
    try:
        return await database.execute(query=query)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=422, detail='Wrong foreign key. Record with set id not in database.')


async def update(payload: dict):
    """Update product with set id in database."""
    query = products.update().where(products.c.product_id == payload['product_id'])
    payload.pop('product_id')
    query = query.values(**payload).returning(products)
    print(query)
    try:
        return await database.fetch_one(query=query)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=422, detail='Wrong foreign key. Record with set id not in database.')


async def delete(product_id: int):
    """Remove product with set id from database.

    All linked orders and order_details are also deleted (cascade).
    """
    query = products.delete().where(products.c.product_id == product_id).returning(products)
    print(query)
    return await database.fetch_one(query=query)
