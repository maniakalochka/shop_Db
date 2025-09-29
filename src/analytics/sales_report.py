import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import aliased

from models.category import Category
from models.order import Order
from models.order_item import OrderItem
from models.product import Product


def top5_products_last_month(sliding: bool = True):
    """
    2.3.1. Отчёт "Топ-5 самых покупаемых товаров за последний месяц"
    :param sliding: True — последние 30 дней, False — календарный предыдущий месяц
    """

    if sliding:
        date_from = datetime.datetime.now - datetime.timedelta(days=30)  # type: ignore
        date_to = None
    else:
        today = datetime.date.today()
        first_this_month = today.replace(day=1)
        date_from = (first_this_month - datetime.timedelta(days=1)).replace(day=1)
        date_to = first_this_month

    RootCategory = aliased(Category)

    stmt = (
        select(
            Product.name.label("product_name"),
            RootCategory.name.label("top_level_category"),
            func.sum(OrderItem.quantity).label("total_qty"),
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .join(Category, Category.id == Product.category_id)
        .join(RootCategory, RootCategory.id == Category.parent_id, isouter=True)  # type: ignore
        .group_by(Product.id, Product.name, RootCategory.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
    )

    if sliding:
        stmt = stmt.where(Order.created_at >= date_from)
    else:
        stmt = stmt.where(Order.created_at >= date_from, Order.created_at < date_to)

    return stmt
