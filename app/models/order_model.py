from sqlalchemy import ForeignKey, Enum as EnumSQL
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base_model import BaseModel
from enum import Enum
from .order_items_model import OrderItem

class OrderModel(BaseModel):
    class StatusPedidos(Enum):
        aguardando_pagamento = "aguardando pagamento"
        confirmado = "confirmado"
        cancelado = "cancelado"
        preparando = "preparando"
        pronto = "pedido pronto"
        envio = "enviado"
        entregue = "entregue"

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[Enum] = mapped_column(EnumSQL(StatusPedidos), default=StatusPedidos.aguardando_pagamento)
    customer_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    total_price: Mapped[float] = mapped_column(nullable=False)

    customer = relationship("CustomerModel", back_populates="orders", lazy="joined")
    order_items = relationship("OrderItem", back_populates="order", lazy="joined", cascade="all, delete-orphan", single_parent=True)