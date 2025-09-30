from sqlalchemy import select, func

from models.client import Client
from models.order import Order
from models.order_item import OrderItem


def client_sales_summary():
    """
    Получение информации о сумме товаров заказанных под каждого клиента
    Результат можно получить через session.execute()
    """
    stmt = (
        select(
            Client.name.label("client_name"),
            func.coalesce(func.sum(OrderItem.quantity * OrderItem.price), 0).label(
                "total_sum"
            ),
        )
        .join(Order, Order.client_id == Client.id)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .group_by(Client.id, Client.name)
        .order_by(Client.name)
    )
    return stmt
