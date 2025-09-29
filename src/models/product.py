from sqlalchemy import ForeignKey, Numeric, String, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base


class Product(Base):
    __tablename__ = "products"

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    category: Mapped["Category"] = relationship(back_populates="products")  # type: ignore
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")  # type: ignore

    __table_args__ = (
        Index("idx_products_category_id", "category_id"),
        Index("idx_products_name", "name"),
    )

    def __repr__(self) -> str:
        return (
            f"Product("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"category_id={self.category_id}, "
            f"quantity={self.quantity}, "
            f"price={self.price})"
        )