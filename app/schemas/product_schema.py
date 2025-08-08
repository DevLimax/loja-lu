from pydantic import BaseModel
from fastapi import Form, Query, Depends
from typing import Optional, List, Union
from typing_extensions import Annotated
from datetime import datetime
from models.product_model import ProductModel

class ProductImagesSchema(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True

class ProductSchemaBase(BaseModel):
    id: Optional[int]
    productName: str
    description: str
    price: float
    barcode: str
    category: ProductModel.Category
    is_avaliable: bool
    quantity: int
    expiration_date: Optional[datetime] = None

    images: List[ProductImagesSchema] = []

    class Config:
        from_attributes = True

class ProductSchemaCreate:
    def __init__(
        self,
        productName: Annotated[str, Form()],
        description: Annotated[str, Form()],
        price: Annotated[float, Form()],
        barcode: Annotated[str, Form()],
        category: Annotated[ProductModel.Category, Form()],
        is_avaliable: Annotated[bool, Form()],
        quantity: Annotated[int, Form()],
        expiration_date: Annotated[Union[datetime, None], Form()] = None
    ):
        self.productName = productName.title()
        self.description = description.title()
        self.price = price
        self.barcode = barcode
        self.category = category
        self.is_avaliable = is_avaliable
        self.quantity = quantity
        self.expiration_date = expiration_date 

class ProductSchemaUpdate:
    def __init__(
        self,
        productName: Annotated[Union[str, None],Form()] = None,
        description: Annotated[Union[str, None],Form()] = None,
        price: Annotated[Union[float, None],Form()] = None,
        barcode: Annotated[Union[str, None],Form()] = None,
        category: Annotated[Union[ProductModel.Category, None],Form()] = None,
        is_avaliabe: Annotated[Union[bool, None],Form()] = None,
        quantity: Annotated[Union[int, None],Form()] = None,
        expiration_date: Annotated[Union[datetime, None],Form()] = None
    ):
        self.productName = productName.title() if productName else None
        self.description = description.title() if description else None
        self.price = price
        self.barcode = barcode
        self.category = category
        self.is_avaliable = is_avaliabe
        self.quantity = quantity
        self.expiration_date = expiration_date


class ProductSchemaFilter(BaseModel):
    category: Optional[ProductModel.Category] = Query(None)
    price: Optional[float] = Query(None)
    is_avaliable: Optional[bool] = Query(None)

    @classmethod
    def as_query(cls):
        def as_form(
            category: Optional[ProductModel.Category] = Query(None),
            price: Optional[float] = Query(None),
            is_avaliable: Optional[bool] = Query(None)
        ):
            return cls(category=category,
                       price=price,
                       is_avaliable=is_avaliable)
        return Depends(as_form)

