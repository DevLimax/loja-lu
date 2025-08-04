from pydantic import BaseModel
from fastapi import Form, Query, Depends
from typing import Optional, List, Union
from datetime import datetime
from models.product_model import ProductModel
from models.order_model import OrderModel

class OrderItemsSchema(BaseModel):
    product_id: int
    quantity: int
    price: Optional[float] = None

    class Config:
        from_attributes = True

class OrderSchemaBase(BaseModel):

    id: Optional[int] = None
    customer_id: int
    status: str
    total_price: float
    created_at: datetime

    order_items: List[OrderItemsSchema]

    class Config:
        from_attributes = True

class OrderschemaCreate(BaseModel):
    customer_id: int
    items: List[OrderItemsSchema]

    class Config:
        from_attributes = True

class OrderSchemaUpdate(BaseModel):
    customer_id: Optional[int] = None
    status: Optional[OrderModel.StatusPedidos] = None,
    total_price: Optional[float] = None

class OrderSchemaFilter(BaseModel):
    status: Optional[OrderModel.StatusPedidos] = Query(None)
    customer_id: Optional[int] = Query(None)
    start_date: Optional[datetime] = Query(None)
    end_date: Optional[datetime] = Query(None)
    category: Optional[ProductModel.Category] = Query(None)

    @classmethod
    def as_query(cls):
        def as_form(
            status: Optional[OrderModel.StatusPedidos] = Query(None),
            customer_id: Optional[int] = Query(None),
            start_date: Optional[datetime] = Query(None),
            end_date: Optional[datetime] = Query(None),
            category: Optional[ProductModel.Category] = Query(None)
        ):
            return cls(
                status = status,
                customer_id = customer_id,
                start_date = start_date,
                end_date = end_date,
                category = category
            )
        return Depends(as_form)
