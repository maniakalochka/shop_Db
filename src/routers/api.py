from fastapi import Depends, APIRouter

from src.db.session import get_async_session
from src.schemas.item import AddItemPayload
from src.services.order_items import add_item_to_order

api_router = APIRouter()


@api_router.post("/orders/{order_id}/items")
async def add_item(
    order_id: int,
    payload: AddItemPayload,
    db=Depends(get_async_session),
):
    item = await add_item_to_order(
        db, order_id=order_id, product_id=payload.product_id, quantity=payload.quantity
    )
    return {"order_item_id": item.id, "quantity": item.quantity}
