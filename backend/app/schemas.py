from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "staff"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerOut(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    sku: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SalesOrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    status: str = "pending"


class SalesOrderCreate(SalesOrderBase):
    pass


class SalesOrderUpdate(BaseModel):
    quantity: Optional[int] = None
    status: Optional[str] = None


class SalesOrderOut(BaseModel):
    id: int
    quantity: int
    total_amount: float
    status: str
    created_at: datetime
    customer_id: int
    product_id: int
    sales_rep_id: Optional[int]

    class Config:
        from_attributes = True
