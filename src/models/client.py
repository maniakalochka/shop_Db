from sqlalchemy import String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base


class Client(Base):
    __tablename__ = "clients"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=True)

    orders: Mapped[list["Order"]] = relationship(back_populates="client")  # type: ignore

    __table_args__ = (Index("idx_clients_name", "name"),)

    def __repr__(self) -> str:
        return (
            f"Client("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"address='{self.address}')"
        )
