from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, AuthResponse

from core.deps import get_current_user, get_session
from core.security import generate_hashed_password
from core.auth import create_access_token, create_refresh_token, verify_refresh_token, authenticate

router = APIRouter()

@router.post("/login", response_model=AuthResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
                db: AsyncSession = Depends(get_session)
) -> JSONResponse:
    """
    Endpoint para efetuar o login do usuário e receber os token de acesso para os demais endpoints.
    """
    user = await authenticate(userInput=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Dados do usuário incorretos"
        )
    
    access_token: str = create_access_token(sub=str(user.id))
    refresh_token: str = create_refresh_token(sub=str(user.id))

    return JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 
        status_code=status.HTTP_200_OK
    )

@router.post("/refresh-token", response_model=AuthResponse)
async def refresh_token(refresh_token: str = Form(...),
                        db: AsyncSession = Depends(get_session),
) -> JSONResponse:
    """
    Endpoint para criar um novo access_token apartir do (refresh_token)
    """
    payload = verify_refresh_token(token=refresh_token)
    if not payload or payload.get("type") != "refresh_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token Inválido"
        )
    
    username = payload.get("sub")
    new_access_token: str = create_access_token(sub=username)
    new_refresh_token: str = create_refresh_token(sub=username)

    return JSONResponse(
        content={
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        },
        status_code=status.HTTP_202_ACCEPTED
    )

@router.post("/register", response_model=UserSchemaBase, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserSchemaCreate, 
                        db: AsyncSession = Depends(get_session)
) -> UserSchemaCreate:
    """
    Endpoint para a criação de um novo usuário no sistema.
    """
    async with db as session:

        new_user = UserModel(
            username=user.username,
            email=user.email,
            password=generate_hashed_password(user.password)
        )

        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        except IntegrityError as e:
            await session.rollback()
            error_Str = str(e).lower()
            if "(email)" in error_Str:
                campo = "email"
            elif "(username)" in error_Str:
                campo = "username"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe um usuário com esse {campo}."
            )
        
        return new_user

@router.get("/logged", response_model=UserSchemaBase)
async def get_me(current_user: UserSchemaBase = Depends(get_current_user)
) -> UserSchemaBase:
    """
    Retorna os dados do usuário logado.
    """
    return current_user