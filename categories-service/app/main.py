from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.api import database, engine, metadata
from app.api.auth import session
from app.api.categories import categories

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/categories/openapi.json", docs_url="/api/categories/docs")
app.add_middleware(PrometheusMiddleware)
app.add_route("/api/categories/metrics", handle_metrics)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await session.close()


app.include_router(categories, prefix='/api/categories', tags=['categories'])
