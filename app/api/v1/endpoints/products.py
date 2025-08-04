from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import Response

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.deps import get_current_user, get_session

from models.product_image import ProductImage
from models.product_model import ProductModel
from models.user_model import UserModel

from schemas.product_schema import ProductSchemaBase, ProductImagesSchema, ProductSchemaCreate, ProductSchemaUpdate, ProductSchemaFilter

from utils.querys_in_db import search_all_items_in_db, search_item_in_db

import os
import shutil
import uuid

router = APIRouter()
UPLOAD_DIR = "static/images_product/"

@router.get("/", response_model=List[ProductSchemaBase], status_code=status.HTTP_200_OK)
async def get_products(db: AsyncSession = Depends(get_session),
                       current_user: UserModel = Depends(get_current_user),
                       filters: ProductSchemaFilter = ProductSchemaFilter.as_query()
) -> List[ProductSchemaBase]:
    
    """
    Retorna todos os produtos cadastrados no banco de dados.

    É possivel filtrar os produtos por Categoria, Preço, Disponibilidade 
    """

    products = await search_all_items_in_db(db=db,
                                            Model=ProductModel,
                                            filters=filters)
    
    return products

@router.get("/{product_id}", response_model=ProductSchemaBase, status_code=status.HTTP_200_OK)
async def get_product(product_id: int,
                      db: AsyncSession = Depends(get_session),
                      current_user: UserModel = Depends(get_current_user)
) -> ProductSchemaBase:
    """
    Retorna um produto especifico pelo ID
    """
    async with db as session:
        product = await search_item_in_db(id=product_id,
                                          db=session,
                                          Model=ProductModel)
        
        if not product:
            raise HTTPException(detail="Produto não encontrado.", status_code=status.HTTP_400_BAD_REQUEST)
        
        return product
    
@router.post("/", response_model=ProductSchemaBase, status_code=status.HTTP_201_CREATED)
async def create_product(productForm: ProductSchemaCreate = Depends(),
                         images: Optional[List[UploadFile]] = File(None),
                         db: AsyncSession = Depends(get_session),
                         current_user: UserModel = Depends(get_current_user)
):
    """
    Endpoint para criação de um novo produto
    """
    async with db as session:
        new_product = ProductModel(
            productName = productForm.productName,
            description = productForm.description,
            category = productForm.category,
            price = productForm.price,
            barcode = productForm.barcode,
            is_avaliable = productForm.is_avaliable,
            quantity = productForm.quantity,
            expiration_date = productForm.expiration_date
        )
        try:
            session.add(new_product)
            await session.flush()

            saved_files = []

            if images:
                for image in images:
                    file_ext = os.path.splitext(image.filename)[1]
                    file_name = f"{uuid.uuid4().hex}{file_ext}"
                    file_path = os.path.join(UPLOAD_DIR, file_name)

                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(image.file, buffer)
                    
                    saved_files.append(file_path)
            else:
                filepath = os.path.join(UPLOAD_DIR, "defaultProduct.png")

            for file in saved_files:
                new_image = ProductImage(
                    product_id = new_product.id,
                    image_url = file
                )
                session.add(new_image)

            await session.commit()
            await session.refresh(new_product)
            return new_product

        except IntegrityError:
            await session.rollback()
            raise HTTPException(detail="Já existe um produto com esse nome.", status_code=status.HTTP_409_CONFLICT)

@router.put("/{product_id}", response_model=ProductSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def update_product(product_id: int,
                         product_form: ProductSchemaUpdate = Depends(),
                         images: Optional[List[UploadFile]] = File(None),
                         db: AsyncSession = Depends(get_session),
                         current_user: UserModel = Depends(get_current_user)
):
    """
    Endpoint para alteração de dados de uma instancia de Produto
    """
    async with db as session:
        product_db = await search_item_in_db(id=product_id,
                                             db=session,
                                             Model=ProductModel)
        
        if not product_db:
            raise HTTPException(detail="Produto não encontrado.", status_code=status.HTTP_400_BAD_REQUEST)
        
        for key, value in product_form.__dict__.items():
            if value is not None:
                setattr(product_db, key, value)

        try: 
            session.add(product_db)

            saved_files = []
            if images:
                for image in images:
                    file_ext = os.path.splitext(image.filename)[1]
                    file_name = f"{uuid.uuid4().hex}{file_ext}"
                    file_path = os.path.join(UPLOAD_DIR, file_name)

                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(image.file, buffer)
                    
                    saved_files.append(file_path)

                for file in saved_files:
                    new_image = ProductImage(
                        product_id = product_db.id,
                        image_url = file
                    )
                    session.add(new_image)
            
            await session.commit()
            await session.refresh(product_db)
            return product_db

        except IntegrityError:
            await session.rollback()
            raise HTTPException(detail="Já existe um produto com esse nome.", status_code=status.HTTP_409_CONFLICT)
            

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int,
                         db: AsyncSession = Depends(get_session),
                         current_user: UserModel = Depends(get_current_user)
) -> Response:
    """
    Deleta uma instancia de produto pelo ID
    """
    product = await search_item_in_db(id=product_id,
                                      db=db,
                                      Model=ProductModel)
    
    if not product:
        raise HTTPException(detail="Produto não encontrado.", status_code=status.HTTP_400_BAD_REQUEST)
    
    await db.delete(product)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)