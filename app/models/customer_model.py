from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .order_model import OrderModel

from .base_model import BaseModel

class CustomerModel(BaseModel):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    cpf: Mapped[str] = mapped_column(unique=True, nullable=False)
    telephone: Mapped[str] = mapped_column(nullable=False)
    
    orders = relationship("OrderModel", back_populates="customer", lazy="joined", cascade="all, delete-orphan")