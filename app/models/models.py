from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime, timedelta

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    sales = relationship("Sale", back_populates="client")
    orders = relationship("Order", back_populates="client")

class Medicine(Base):
    __tablename__ = 'medicines'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    generic_name = Column(String)
    manufacturer = Column(String)
    type = Column(String)
    pharmaceutical_form = Column(String)
    lote = Column(String)
    fabricacao = Column(Date)
    validade = Column(Date)
    fornecedor = Column(String)
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

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey('medicines.id'))
    quantity = Column(Integer)
    price = Column(Float)
    session_id = Column(String, index=True)
    
    medicine = relationship("Medicine")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    total_price = Column(Float)
    order_date = Column(DateTime, default=lambda: datetime.now() - timedelta(hours=3))
    
    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    medicine_id = Column(Integer, ForeignKey('medicines.id'))
    quantity = Column(Integer)
    price = Column(Float)
    
    order = relationship("Order", back_populates="items")
    medicine = relationship("Medicine")