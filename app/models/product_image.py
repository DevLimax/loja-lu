from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from core.configs import settings

class ProductImage(settings.DBBASEMODEL):
    __tablename__ = "produto_fotos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    image_url: Mapped[str] = mapped_column(nullable=False)

    product = relationship("ProductModel", back_populates="images", lazy="joined")
