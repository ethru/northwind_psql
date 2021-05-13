from fastapi import FastAPI
from elasticapm.contrib.starlette import ElasticAPM
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.api import database, engine, metadata
from app.api.auth import session
from app.api.products import products, apm

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/products/openapi.json", docs_url="/api/products/docs")
app.add_middleware(PrometheusMiddleware)
app.add_route("/api/products/metrics", handle_metrics)

app.add_middleware(ElasticAPM, client=apm)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await session.close()


app.include_router(products, prefix='/api/products', tags=['products'])
