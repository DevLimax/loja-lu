from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.configs import settings

class OrderItem(settings.DBBASEMODEL):
    __tablename__ = "pedido_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    price: Mapped[float] = mapped_column(nullable=False)

    order = relationship("OrderModel", back_populates="order_items", lazy="joined")
    product = relationship("ProductModel", back_populates="order_items", lazy="joined")

