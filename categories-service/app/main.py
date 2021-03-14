from fastapi import FastAPI

from app.api import database, engine, metadata
from app.api.categories import categories

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/categories/openapi.json", docs_url="/api/categories/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(categories, prefix='/api/categories', tags=['categories'])
