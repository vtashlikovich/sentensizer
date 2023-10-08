from .db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    author = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Shop(Base):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), unique=True, index=True)
    available_quantity = Column(Integer, default=0)
    initial_quantity = Column(Integer)
    price = Column(Integer)

    book = relationship("Book")


class Basket(Base):
    __tablename__ = "basket"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    shop_id = Column(Integer, ForeignKey("shop.id"))
    quantity = Column(Integer, default=0)
    price = Column(Integer)

    shop = relationship("Shop")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    total_price = Column(Integer)
    status = Column(Integer)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime

    orderitems = relationship("OrderItem")


class OrderItem(Base):
    __tablename__ = "orderitem"

    id = Column(Integer, primary_key=True, index=True)
    shopitem_id = Column(Integer, ForeignKey("shop.id"))
    order_id = Column(Integer, ForeignKey("order.id"))
    quantity = Column(Integer)
    price = Column(Integer)

    shopitem = relationship("Shop")
