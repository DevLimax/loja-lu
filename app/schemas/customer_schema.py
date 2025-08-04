from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import Query, Depends

class CustomerSchemaBase(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: EmailStr
    cpf: str
    telephone: str

class CustomerSchemaUpdate(CustomerSchemaBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    telephone: Optional[str] = None

class CustomerSchemaFilter(BaseModel):
    first_name: Optional[str] = Query(None)
    last_name: Optional[str] = Query(None)
    email: Optional[EmailStr] = Query(None)
    cpf: Optional[str] = Query(None)

    @classmethod
    def as_query(cls):
        def as_form(
            first_name: Optional[str] = Query(None),
            last_name: Optional[str] = Query(None),
            email: Optional[EmailStr] = Query(None),
            cpf: Optional[str] = Query(None)
        ):
            return cls(first_name=first_name,
                       last_name=last_name,
                       email=email,
                       cpf=cpf)
        return Depends(as_form)
            