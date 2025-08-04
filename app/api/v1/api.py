from fastapi import APIRouter
from api.v1.endpoints import user, customer, products, orders, messages

router = APIRouter()

router.include_router(user.router, prefix="/auth", tags=["Autenticação"])
router.include_router(customer.router, prefix="/customers", tags=["Clientes"])
router.include_router(products.router, prefix="/products", tags=["Produtos"])
router.include_router(orders.router, prefix="/orders", tags=["Pedidos"])
router.include_router(messages.router, prefix="/messages", tags=["Mensagens"])


