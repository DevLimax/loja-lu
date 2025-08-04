from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from core.db import Session
from core.auth import oauth2_schema
from core.configs import settings
from utils.querys_in_db import search_item_in_db
from models.user_model import UserModel

class TokenData(BaseModel):
    username: str

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = Session()

    try: 
        yield session
    finally:
        await session.close()

async def get_current_user(db: AsyncSession = Depends(get_session),
                           token: str = Depends(oauth2_schema)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possivel autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try: 
        payload = jwt.decode(token=token, 
                             key=settings.JWT_SECRET,
                             algorithms=[settings.ALGORITHM],
                             options={"verify_aud": False}
    )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    
    async with db as session:
        user = await search_item_in_db(id=int(token_data.username), 
                                       Model=UserModel,
                                       db=session)
        if user is None:
            raise credentials_exception
        
        return user
    

    

