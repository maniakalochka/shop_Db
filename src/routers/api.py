from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.db.session import SessionLocal
from src.schemas.item import AddItemPayload
from src.services.order_items import add_item_to_order

app = FastAPI()


@app.post("/orders/{order_id}/items")
def add_item(
    order_id: int, payload: AddItemPayload, db: Session = Depends(SessionLocal)
) -> dict[str, int]:
    item = add_item_to_order(
        db, order_id=order_id, product_id=payload.product_id, quantity=payload.quantity
    )
    return {"order_item_id": item.id, "quantity": item.quantity}
