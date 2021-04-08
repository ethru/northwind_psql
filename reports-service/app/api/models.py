from datetime import date

from pydantic import BaseModel, validator
from sqlalchemy import Column, Date, Float, ForeignKeyConstraint, Integer, String, Table

from app.api import metadata

categories = Table(
    'categories',
    metadata,
    Column('category_id', String, primary_key=True),
    Column('category_name', String)
)

customers = Table(
    'customers',
    metadata,
    Column('customer_id', String, primary_key=True),
    Column('company_name', String)
)

employees = Table(
    'employees',
    metadata,
    Column('employee_id', Integer, primary_key=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('title', String),
    Column('title_of_courtesy', String)
)

orders = Table(
    'orders',
    metadata,
    Column('order_id', Integer, primary_key=True),
    Column('customer_id', String),
    Column('employee_id', Integer),
    Column('order_date', Date),
    Column('required_date', Date),
    Column('shipped_date', Date),
    Column('ship_via', Integer),
    Column('freight', Float),
    Column('ship_name', String),
    Column('ship_address', String),
    Column('ship_city', String),
    Column('ship_region', String),
    Column('ship_postal_code', String),
    Column('ship_country', String),
    Column('paypal_id', String),
    Column('status', String),
    ForeignKeyConstraint(['customer_id'], ['customers.customer_id']),
    ForeignKeyConstraint(['employee_id'], ['employees.employee_id']),
    ForeignKeyConstraint(['ship_via'], ['shippers.shipper_id'])
)

order_details = Table(
    'order_details',
    metadata,
    Column('order_id', Integer, primary_key=True),
    Column('product_id', Integer, primary_key=True),
    Column('unit_price', Integer),
    Column('quantity', Integer),
    Column('discount', Integer),
    ForeignKeyConstraint(['order_id'], ['orders.order_id']),
    ForeignKeyConstraint(['product_id'], ['products.product_id'])
)

products = Table(
    'products',
    metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('supplier_id', Integer),
    Column('category_id', Integer),
    Column('quantity_per_unit', String),
    Column('unit_price', Integer),
    Column('units_in_stock', Integer),
    Column('units_on_order', Integer),
    Column('reorder_level', Integer),
    Column('discontinued', Integer),
    ForeignKeyConstraint(['supplier_id'], ['suppliers.supplier_id']),
    ForeignKeyConstraint(['category_id'], ['categories.category_id'])
)

suppliers = Table(
    'suppliers',
    metadata,
    Column('supplier_id', String, primary_key=True),
    Column('company_name', String),
    Column('contact_name', String),
    Column('contact_title', String),
    Column('phone', String),
)


class Date(BaseModel):
    from_date: date
    to_date: date

    @validator('to_date')
    def to_date_must_be_less_than_today(cls, to_date):
        if to_date > date.today():
            raise ValueError('to date must be less than today\'s date')
        return to_date

    @validator('to_date')
    def to_date_cannot_be_greater_than_today(cls, to_date, values):
        from_date = values.get('from_date')
        if from_date:
            if from_date > to_date:
                raise ValueError('to date must be greater or equal from date')
            return to_date


class Employee(BaseModel):
    employee_id: int
    employee: str
    title: str
    orders: int


class Customer(BaseModel):
    customer_id: str
    company_name: str
    profit: int


class Product(BaseModel):
    product_id: int
    product_name: str
    category_name: str


class ProductPopular(Product):
    sold: int


class ProductReorder(Product):
    units_in_stock: int
    units_on_order: int
    units_available: int
    reorder_level: int
    supplier: str
    contact: str
