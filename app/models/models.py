from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    sales = relationship("Sale", back_populates="client")

class Medicine(Base):
    __tablename__ = 'medicines'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, index=True)
    price = Column(Float, index=True)
    sales = relationship("Sale", back_populates="medicine")

class UserModel(Base):
    __tablename__= "users"
    id= Column(Integer, primary_key=True, autoincrement=True)
    username=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    medicine_id = Column(Integer, ForeignKey('medicines.id'))
    quantity = Column(Integer)
    total_price = Column(Float)
    sale_date = Column(DateTime, default=datetime.utcnow)
    
    client = relationship("Client", back_populates="sales")
    medicine = relationship("Medicine", back_populates="sales")