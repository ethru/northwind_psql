from os import getenv
from typing import List

from elasticapm.contrib.starlette import make_apm_client
from fastapi import APIRouter, Depends
from prometheus_client import Summary

from app.api import db
from app.api.auth import authorize
from app.api.models import Date, Customer, Employee, ProductPopular, ProductReorder

reports = APIRouter()

request_metrics = Summary('request_processing_seconds', 'Time spent processing request')

apm = make_apm_client({'SERVICE_NAME': 'Reports', 'SERVER_URL': getenv('APM_URL')})


@request_metrics.time()
@reports.post('/customers/profit', response_model=List[Customer], dependencies=[Depends(authorize)])
async def get_profit_by_customer(payload: Date):
    """Return total profit from customer in set period of time."""
    apm.capture_message('Profit report generated.')
    return await db.get_sales_by_customer(**payload.dict())


@request_metrics.time()
@reports.post('/employees/activity', response_model=List[Employee], dependencies=[Depends(authorize)])
async def get_employees_activity(payload: Date):
    """Return employees activity in set period of time."""
    apm.capture_message('Activity report generated.')
    return await db.get_employees_activity(**payload.dict())


@request_metrics.time()
@reports.post('/employees/delays', response_model=List[Employee], dependencies=[Depends(authorize)])
async def get_employees_shipment_delays(payload: Date):
    """Return employees shipment delays in set period of time."""
    apm.capture_message('Delays report generated.')
    return await db.get_employees_shipment_delays(**payload.dict())


@request_metrics.time()
@reports.post('/products/popularity', response_model=List[ProductPopular], dependencies=[Depends(authorize)])
async def get_products_sales(payload: Date):
    """Return total number of each sold product in set period of time."""
    apm.capture_message('Popularity report generated.')
    return await db.get_products_by_popularity(**payload.dict())


@request_metrics.time()
@reports.get('/products/reorder', response_model=List[ProductReorder], dependencies=[Depends(authorize)])
async def get_products_to_reorder():
    """Return report about products to reorder."""
    apm.capture_message('Reorder report generated.')
    return await db.get_products_to_reorder()
