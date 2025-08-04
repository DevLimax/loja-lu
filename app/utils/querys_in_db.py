from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from core.configs import settings
from models.order_model import OrderModel
from models.order_items_model import OrderItem
from models.product_model import ProductModel
from typing import Optional, Type

async def search_item_in_db(id: int, 
                            Model: Type[DeclarativeMeta], 
                            db: AsyncSession,
):
    """
    Função para buscar um item no banco de dados pelo ID.
    """ 
    query = select(Model).filter(Model.id == id )
    result = await db.execute(query)
    item = result.scalars().unique().one_or_none()
    return item

async def search_all_items_in_db(Model: Type[DeclarativeMeta],
                                 db: AsyncSession,
                                 filters: Optional[dict] = None,
                                 skip: int = 0,
                                 limit: int = 10
):
    query = select(Model).order_by(Model.id)
    if filters:

        if Model == OrderModel and filters.category:
            query = query.join(OrderModel.order_items)
            query = query.join(OrderItem.product)
            query = query.where(ProductModel.category == filters.category)
            query = query.distinct()

        if Model == OrderModel and filters.start_date and filters.end_date:
            start_date = filters.start_date
            end_date = filters.end_date
            query = query.where(Model.created_at.between(start_date, end_date))
        elif Model == OrderModel and filters.start_date:
            start_date = filters.start_date
            query = query.where(Model.created_at >= start_date)
        elif Model == OrderModel and filters.end_date:
            end_date = filters.end_date
            query = query.where(Model.created_at <= end_date)

        for atrr, value in filters.dict(exclude_none=True).items():
            try: 
                column = getattr(Model, atrr)
            except AttributeError:
                continue
            
            if column is not None:
                if isinstance(value, str) and atrr != "category":
                    query = query.where(column.ilike(f"%{value}%"))
                else:
                    query = query.where(column == value)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    list_items = result.scalars().unique().all()
    return list_items
