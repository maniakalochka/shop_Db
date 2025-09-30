from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.product import Product


async def add_item_to_order(
    db: AsyncSession, order_id: int, product_id: int, quantity: int
) -> OrderItem:
    """Добавление товара в заказ с проверками (асинхронная версия)"""

    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    # Проверка заказа
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Блокируем товар для корректного уменьшения stock
    result = await db.execute(
        select(Product).where(Product.id == product_id).with_for_update()
    )
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.quantity < quantity:
        raise HTTPException(status_code=409, detail="Not enough stock")

    # Проверяем, есть ли уже этот товар в заказе
    result = await db.execute(
        select(OrderItem).where(
            OrderItem.order_id == order_id,
            OrderItem.product_id == product_id,
        )
    )
    order_item = result.scalar_one_or_none()

    if order_item:
        order_item.quantity += quantity
    else:
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=product.price,
        )
        db.add(order_item)

    # Обновляем остатки
    product.quantity -= quantity

    await db.commit()
    await db.refresh(order_item)

    return order_item


# from fastapi import HTTPException
# from sqlalchemy import select
# from sqlalchemy.orm import Session
#
# from src.models.order import Order
# from src.models.order_item import OrderItem
# from src.models.product import Product
#
#
# def add_item_to_order(
#     db: Session, order_id: int, product_id: int, quantity: int
# ) -> OrderItem:
#     """Добавление товара в заказ с проверками"""
#
#     if quantity <= 0:
#         raise HTTPException(status_code=400, detail="Quantity must be positive")
#
#     order = db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()
#     if order is None:
#         raise HTTPException(status_code=404, detail="Order not found")
#
#     product = db.execute(
#         select(Product).where(Product.id == product_id).with_for_update()
#     ).scalar_one_or_none()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#
#     if product.quantity < quantity:
#         raise HTTPException(status_code=409, detail="Not enough stock")
#
#     order_item = db.execute(
#         select(OrderItem).where(
#             OrderItem.order_id == order_id, OrderItem.product_id == product_id
#         )
#     ).scalar_one_or_none()
#
#     if order_item:
#         order_item.quantity += quantity
#     else:
#         order_item = OrderItem(
#             order_id=order_id,
#             product_id=product_id,
#             quantity=quantity,
#             price=product.price,
#         )
#         db.add(order_item)
#
#     product.quantity -= quantity
#
#     db.commit()
#     db.refresh(order_item)
#     return order_item
