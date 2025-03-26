from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    email: str
    phone: str

class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True

class ClientCreate(ClientBase):
    pass


class MedicineBase(BaseModel):
    name: str
    quantity: int
    price: float

class Medicine(MedicineBase):
    id: int

    class Config:
        orm_mode = True

class MedicineCreate(MedicineBase):
    pass

class User(BaseModel):
    username: str
    password: str