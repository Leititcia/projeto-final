from sqlalchemy import Column, Integer, String, Float
from database.database import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)

class Medicine(Base):
    __tablename__ = 'medicines'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, index=True)
    price = Column(Float, index=True)

class UserModel(Base):
    __tablename__= "users"
    id= Column(Integer, primary_key=True, autoincrement=True)
    username=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)