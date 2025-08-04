from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr

class UserSchemaCreate(UserSchemaBase):
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str