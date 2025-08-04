from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import Response

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.deps import get_current_user, get_session

from models.product_model import ProductModel
from models.order_model import OrderModel
from models.order_items_model import OrderItem
from models.customer_model import CustomerModel
from models.user_model import UserModel

from schemas.order_schema import OrderItemsSchema, OrderSchemaBase, OrderschemaCreate, OrderSchemaUpdate, OrderSchemaFilter

from utils.querys_in_db import search_all_items_in_db, search_item_in_db
from WhatsappAPI.messages.orders_messages import send_message_new_order, send_message_update_status

router = APIRouter()

@router.get("/", response_model=List[OrderSchemaBase], status_code=status.HTTP_200_OK)
async def get_orders(db: AsyncSession = Depends(get_session),
                     current_user: UserModel = Depends(get_current_user),
                     filters: OrderSchemaFilter = OrderSchemaFilter.as_query()
) -> List[OrderSchemaBase]:
    
    orders = await search_all_items_in_db(db=db,
                                          Model=OrderModel,
                                          filters=filters)
    
    return orders

@router.get("/{order_id}", response_model=OrderSchemaBase, status_code=status.HTTP_200_OK)
async def get_order(order_id: int,
                    db: AsyncSession = Depends(get_session),
                    current_user: UserModel = Depends(get_current_user)
) -> OrderSchemaBase:

    async with db as session:
        order = await search_item_in_db(id=order_id,
                                        db=session,
                                        Model=OrderModel)
        
        if not order:
            raise HTTPException(detail="Pedido não encontrado", 
                                status_code=status.HTTP_400_BAD_REQUEST)
        
        return order
    
@router.post("/", response_model=OrderSchemaBase, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderschemaCreate,
                       db: AsyncSession = Depends(get_session),
                       current_user: UserModel = Depends(get_current_user)
) -> OrderSchemaBase:

    total_price = 0
    for item in order.items:
        if not item.price:
            product_db: ProductModel = await search_item_in_db(id=item.product_id,
                                                 db=db,
                                                 Model=ProductModel)
            if not product_db:
                raise HTTPException(detail=f"Produto #{item.product_id} não encontrado",
                              status_code=status.HTTP_400_BAD_REQUEST)
                
            total_price += product_db.price * item.quantity
        else:
            total_price += item.price

    async with db as session:
        customer: CustomerModel = await search_item_in_db(id=order.customer_id,
                                           db=session,
                                           Model=CustomerModel)
        if not customer:
            raise HTTPException(detail="Cliente não encontrado",
                                status_code=status.HTTP_400_BAD_REQUEST)
        
        new_order = OrderModel(
            customer_id = order.customer_id,
            total_price = total_price
        )
        session.add(new_order)
        await session.flush()

        for item in order.items:
            product: ProductModel = await search_item_in_db(id=item.product_id,
                                              db=session,
                                              Model=ProductModel)
            
            if not product.is_avaliable:
                raise HTTPException(detail=f"Produto ({product.id} - {product.productName}) Indisponivel",
                                    status_code=status.HTTP_400_BAD_REQUEST)
            elif product and product.is_avaliable:
                if not item.price:
                    item.price = product.price * item.quantity

                if item.quantity > product.quantity:
                    raise HTTPException(detail=f"Produto ({product.id} - {product.productName}) Não tem estoque suficiente, por favor reveja a quantidade disponivel.", 
                                        status_code=status.HTTP_400_BAD_REQUEST)
                
                order_item = OrderItem(
                    order_id = new_order.id,
                    product_id = product.id,
                    quantity = item.quantity,
                    price = item.price
                )

                product.quantity -= item.quantity
                if product.quantity <= 0:
                    product.is_avaliable = False

                try:
                    session.add(order_item)
                    session.add(product)
                except IntegrityError as e:
                    await session.rollback()
                    print("Houve um error", e)
                    return HTTPException(detail="Error não identificado", status_code=status.HTTP_400_BAD_REQUEST)

        await session.commit()
        await session.refresh(new_order)

        products_str = "\n  ".join([f"- {item.quantity} X {item.product.productName}" for item in new_order.order_items])
        await send_message_new_order(number=new_order.customer.telephone,
                                     order=new_order,
                                     products_str=products_str)
        return new_order

@router.put("/{order_id}", response_model=OrderSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def update_order(order_id: int,
                       order_data: OrderSchemaUpdate,
                       db: AsyncSession = Depends(get_session),
                       current_user: UserModel = Depends(get_current_user)
) -> OrderSchemaBase:
    
    async with db as session:
        order_db: OrderModel = await search_item_in_db(id=order_id,
                                           db=session,
                                           Model=OrderModel)
        
        if not order_db:
            raise HTTPException(detail="Pedido não encontrado",
                                status_code=status.HTTP_400_BAD_REQUEST)
        
        status_is_modified = False

        for key, value in order_data.dict(exclude_unset=True).items():
            if key == "status":
                if value != order_db.status:
                    status_is_modified = True
            setattr(order_db, key, value)

        if order_db.status == OrderModel.StatusPedidos.cancelado:
            print("Restaurando estoque")
            for item in order_db.order_items:
                item: OrderItem
                product: ProductModel = await search_item_in_db(id=item.product_id,
                                                                db=session,
                                                                Model=ProductModel)
                product.quantity += item.quantity
                print(product.quantity)
                if product.quantity > 0:
                    product.is_avaliable = True
                session.add(product)

        session.add(order_db)
        await session.commit()
        await session.refresh(order_db)
        if status_is_modified:
            await send_message_update_status(number=order_db.customer.telephone,
                                             order=order_db)
        return order_db
    
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id:int,
                       db: AsyncSession = Depends(get_session),
                       current_user: UserModel = Depends(get_current_user)
) -> Response:
    
    order = await search_item_in_db(id=order_id,
                                    db=db,
                                    Model=OrderModel)
    
    if not order:
        raise HTTPException(detail="Pedido não encontrado", 
                            status_code=status.HTTP_400_BAD_REQUEST)
    
    await db.delete(order)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)