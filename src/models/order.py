import datetime

from sqlalchemy import ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )

    client: Mapped["Client"] = relationship(back_populates="orders")  # type: ignore
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")  # type: ignore

    __table_args__ = (
        Index("idx_orders_client_id", "client_id"),
        Index("idx_orders_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            f"Order("
            f"id={self.id}, "
            f"client_id={self.client_id}, "
            f"created_at='{self.created_at}')"
        )
