from fastapi import FastAPI
from elasticapm.contrib.starlette import ElasticAPM
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.api import database, engine, metadata
from app.api.auth import session
from app.api.reports import reports, apm

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/reports/openapi.json", docs_url="/api/reports/docs")
app.add_middleware(PrometheusMiddleware)
app.add_route("/api/reports/metrics", handle_metrics)

app.add_middleware(ElasticAPM, client=apm)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await session.close()


app.include_router(reports, prefix='/api/reports', tags=['reports'])
