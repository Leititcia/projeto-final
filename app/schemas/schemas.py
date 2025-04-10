from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClientBase(BaseModel):
    name: str
    email: str
    phone: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True

class MedicineBase(BaseModel):
    name: str
    quantity: int
    price: float

class Medicine(MedicineBase):
    id: int

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    client_id: int
    medicine_id: int
    quantity: int

class Sale(SaleBase):
    id: int
    total_price: float
    sale_date: datetime
    client: Client
    medicine: Medicine

    class Config:
        from_attributes = True