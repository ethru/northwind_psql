from fastapi import HTTPException

from app.api import database
from app.api.models import categories, CategoryIn, CategoryOut


async def get_category(category_id: int):
    """Get category with set id from database."""
    return await database.fetch_one(query=categories.select().where(categories.c.category_id == category_id))


async def get_categories():
    """Get all categories stored in database."""
    return await database.fetch_all(query=categories.select())


async def add_category(payload: CategoryIn):
    """Store new category in database."""
    query = categories.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_unlisted_category_id():
    """Return id of UNLISTED category.

    If category does not exist then create it.
    """
    name = 'UNLISTED'
    unlisted = await database.fetch_one(query=categories.select().where(categories.c.category_name == name))
    if unlisted:
        return unlisted['category_id']

    unlisted = CategoryIn(category_name=name, description='', picture='')
    return await add_category(unlisted)


async def update(payload: dict):
    """Update category with set id in database."""
    query = categories.update().where(categories.c.category_id == payload['category_id'])
    payload.pop('category_id')
    query = query.values(**payload).returning(categories)
    return await database.fetch_one(query=query)


@database.transaction()
async def delete(category_id: int):
    """Remove category with set id from database.

    Unlink all products connected to that category by replacing category_id with id of unlisted category.
    """
    if not await get_category(category_id):
        raise HTTPException(status_code=404, detail='Category not found.')

    empty = await get_unlisted_category_id()
    query = "UPDATE products SET category_id = :empty WHERE category_id = :id"
    await database.execute(query=query, values={'empty': empty, 'id': category_id})

    query = categories.delete().where(categories.c.category_id == category_id).returning(categories)
    return await database.fetch_one(query=query)
