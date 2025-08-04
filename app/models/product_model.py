from sqlalchemy import String, Integer, Float, ForeignKey, Boolean, DateTime, Enum as EnumSQL
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base_model import BaseModel
from enum import Enum
from datetime import datetime

class ProductModel(BaseModel):

    class Category(str, Enum):
        blusa = "blusa"
        short = "short"
        camiseta = "camiseta"
        overSized = "overSized"
        calça = "calça"

    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    productName: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    barcode: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[Enum] = mapped_column(EnumSQL(Category, name="categorias"), nullable=False)
    is_avaliable: Mapped[bool] = mapped_column(default=True)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(nullable=True)

    order_items = relationship("OrderItem", back_populates="product", lazy="joined", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", lazy="joined", cascade="all, delete-orphan")

    
    