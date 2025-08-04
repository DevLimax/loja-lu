from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.deps import get_current_user, get_session

from models.user_model import UserModel
from models.customer_model import CustomerModel
from schemas.customer_schema import CustomerSchemaBase, CustomerSchemaUpdate, CustomerSchemaFilter

from utils.querys_in_db import search_item_in_db, search_all_items_in_db

router = APIRouter()

@router.get("/", response_model=List[CustomerSchemaBase], status_code=status.HTTP_200_OK)
async def get_clients(db: AsyncSession = Depends(get_session),
                      current_user: UserModel = Depends(get_current_user),
                      filters: CustomerSchemaFilter = CustomerSchemaFilter.as_query(),
                      skip: Optional[int] = 0,
                      limit: Optional[int] = 10,
) -> List[CustomerSchemaBase]:
    """
    Retorna uma lista de todos os clientes registrados no banco de dados, 
    caso não haja nada, a lista é retornada sem valor -> []
    """
    
    customers = await search_all_items_in_db(db=db, 
                                             Model=CustomerModel,
                                             filters=filters,
                                             skip=skip,
                                             limit=limit)
    
    return customers

@router.get("/{customer_id}", response_model=CustomerSchemaBase, status_code=status.HTTP_200_OK)
async def get_client(customer_id: int,
                     db: AsyncSession = Depends(get_session),
                     current_user: UserModel = Depends(get_current_user)) -> CustomerSchemaBase:
    
    """Retorna um cliente especifico apartir do ID"""
    
    customer = await search_item_in_db(db=db, 
                                       Model=CustomerModel, 
                                       id=customer_id)
    
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    
    return customer

@router.post("/", response_model=CustomerSchemaBase, status_code=status.HTTP_201_CREATED)
async def create_client(customer: CustomerSchemaBase,
                        db: AsyncSession = Depends(get_session),
                        current_user: UserModel = Depends(get_current_user)
) -> CustomerSchemaBase:
    
    """
    Endpoint para criação de um novo cliente no sistema.\n
    O endpoint valida os campos Email e CPF que devem ser unicos para cada instancia de cliente.
    """
    
    async with db as session:
        new_customer = CustomerModel(**customer.dict())

        if len(new_customer.cpf) > 11 or len(new_customer.cpf) < 11:
            raise HTTPException(detail="O CPF inserido é invalido!",
                                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if len(new_customer.telephone) < 12 or len(new_customer.telephone) > 14:
            raise HTTPException(detail="O Número inserido é invalido!",
                                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        new_customer.first_name = new_customer.first_name.title()
        new_customer.last_name = new_customer.last_name.title()

        try:
            session.add(new_customer)
            await session.commit()
            await session.refresh(new_customer)
        except IntegrityError as e:
            await session.rollback()
            error_str = str(e).lower()
            if "(email)" in error_str:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
            elif "(cpf)" in error_str:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado")
            elif "(telephone)" in error_str:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Telefone já cadastrado")
            
        return new_customer
    
@router.put("/{customer_id}", response_model=CustomerSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def update_client(customer_id: int,
                        customerForm: CustomerSchemaUpdate,
                        db: AsyncSession = Depends(get_session),
                        current_user: UserModel = Depends(get_current_user)
) -> CustomerSchemaBase:
    
    """
    Endpoint para alterar dados de uma cliente especifico por meio do ID.
    
    Todos os campos estão opcionais.

    O endpoint valida se o EMAIL ou CPF alterado ja existe na base de dados do sistema.
    """
    
    async with db as session:
        customer_up = await search_item_in_db(db=db, Model=CustomerModel, id=customer_id)

        if not customer_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
        
        for key, value in customerForm.dict(exclude_unset=True).items():
            if key == "first_name" or key == "last_name":
                value = value.title()

            if key == "cpf":
                if len(value) < 11 or len(value) > 11:
                    raise HTTPException(detail="O CPF inserido é invalido!",
                                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            if key == "telephone":
                if len(value) < 12 or len(value) > 14:
                    raise HTTPException(detail="O Número inserido é invalido!",
                                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

            setattr(customer_up, key, value)

        try:
            session.add(customer_up)
            await session.commit()
            await session.refresh(customer_up)
        except IntegrityError as e:
            await session.rollback()
            error_str = str(e).lower()
            if "(email)" in error_str:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
            elif "(cpf)" in error_str:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado")
            elif "(telephone)" in error_str:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Telefone já cadastrado")
            
        return customer_up
    
@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(customer_id: int,
                        db: AsyncSession = Depends(get_session),
                        current_user: UserModel = Depends(get_current_user)
) -> Response:
    """
    Endpoint para deletar um cliente apartir do ID escolhido.
    """
    
    customer = await search_item_in_db(db=db, Model=CustomerModel, id=customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
        
    await db.delete(customer)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


    
    


