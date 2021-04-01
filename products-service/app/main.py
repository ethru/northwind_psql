from fastapi import FastAPI

from app.api import database, engine, metadata
from app.api.auth import session
from app.api.products import products

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/products/openapi.json", docs_url="/api/products/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await session.close()


app.include_router(products, prefix='/api/products', tags=['products'])
