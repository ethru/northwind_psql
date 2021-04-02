from fastapi import FastAPI

from app.api import database, engine, metadata
from app.api.auth import session
from app.api.reports import reports

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/reports/openapi.json", docs_url="/api/reports/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await session.close()


app.include_router(reports, prefix='/api/reports', tags=['reports'])
