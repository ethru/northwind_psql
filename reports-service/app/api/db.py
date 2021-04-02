from app.api import database
from app.api.models import categories, order_details, orders, products, suppliers

from sqlalchemy.sql import and_, desc, func, join, select, text


async def get_products_by_popularity(from_date, to_date):
    """Return report about products by popularity in set period of time."""
    query = select(
        [
            order_details.c.product_id,
            products.c.product_name,
            categories.c.category_name,
            func.sum(order_details.c.quantity).label('sold')
        ]
    ).select_from(
        join(join(join(orders, order_details, orders.c.order_id == order_details.c.order_id),
                  products, products.c.product_id == order_details.c.product_id),
             categories, products.c.category_id == categories.c.category_id)
    ).where(
        and_(
            orders.c.order_date >= from_date,
            orders.c.order_date <= to_date,
        )
    ).group_by(
        order_details.c.product_id,
        products.c.product_name,
        categories.c.category_name,
    ).order_by(
        desc('sold')
    )
    print(query)
    return await database.fetch_all(query=query)


async def get_products_to_reorder():
    """Return report about products to reorder."""
    available = products.c.units_in_stock - products.c.units_on_order
    contact = func.concat(suppliers.c.contact_title, text("': '"), suppliers.c.contact_name,
                          text("' via '"), suppliers.c.phone)
    to_reorder = available - products.c.reorder_level

    query = select(
        [
            products.c.product_id,
            products.c.product_name,
            categories.c.category_name,
            products.c.units_in_stock,
            products.c.units_on_order,
            available.label('units_available'),
            products.c.reorder_level,
            suppliers.c.company_name.label('supplier'),
            contact.label('contact')
        ]
    ).select_from(
        join(join(products, suppliers, products.c.supplier_id == suppliers.c.supplier_id),
             categories, products.c.category_id == categories.c.category_id)
    ).where(
        and_(
            products.c.discontinued == 0,
            to_reorder <= 0
        )
    )
    print(query)
    return await database.fetch_all(query=query)
