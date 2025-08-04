import requests
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import Response, JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from models.customer_model import CustomerModel
from models.order_model import OrderModel
from models.product_model import ProductModel
from models.product_image import ProductImage

from core.deps import get_current_user, get_session

from utils.querys_in_db import search_all_items_in_db, search_item_in_db
from WhatsappAPI.messages.orders_messages import send_message_new_order
from WhatsappAPI.messages.alternatives_messages import send_message_promotion_product


router = APIRouter()

@router.post("/send_order/{order_id}", status_code=status.HTTP_201_CREATED)
async def send_new_order(order_id: int,
                         db: AsyncSession = Depends(get_session)
):
    order: OrderModel = await search_item_in_db(id=order_id,
                                    db=db,
                                    Model=OrderModel)
    
    if not order: 
        raise HTTPException(detail=f"Não foi possivel encontrar o pedido de ID #{order_id}",
                      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    products_str = "\n  ".join([f"- {item.quantity} X {item.product.productName}" for item in order.order_items])
        
    try:
        message = await send_message_new_order(number=order.customer.telephone,
                                         order=order,
                                         products_str=products_str)
        
        if message:
            return JSONResponse(content={"message": "Mensagem enviada com sucesso."},
                         status_code=status.HTTP_201_CREATED)
        else:
            return JSONResponse(content={"message": "Houve um erro ao enviar a mensagem"},
                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    except Exception as e:
        raise HTTPException(detail=f"Erro inesperado: {e}",
                      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.post("/send_promotion/{product_id}", status_code=status.HTTP_201_CREATED)
async def send_promotion(product_id: int,
                         customer_id: int = Form(...),
                         promotion_price: float = Form(...),
                         db: AsyncSession = Depends(get_session)
):
    async with db as session:
        product: ProductModel = await search_item_in_db(id=product_id,
                                                        db=session,
                                                        Model=ProductModel)
        
        customer: CustomerModel = await search_item_in_db(id=customer_id,
                                                          db=session,
                                                          Model=CustomerModel)
        if not product:
            raise HTTPException(detail="Produto não encontrado.",
                                status_code=status.HTTP_400_BAD_REQUEST)

        response = await send_message_promotion_product(number=customer.telephone,
                                             product=product,   
                                             promotion_price=promotion_price)

        if response.status_code == 201:
            return JSONResponse(content={"Message": "Mensagem enviada"}, status_code=status.HTTP_201_CREATED)

        else:
            return JSONResponse(content={"Error ao enviar mensagem": f"{response.text} - {response.status_code}"})
        