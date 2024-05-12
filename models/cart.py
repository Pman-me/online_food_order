from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class CartModel(BaseModel):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_price = Column(Float, nullable=False, default=0)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='cascade', onupdate='cascade'))
    items = relationship('CartItemModel', backref='cart')
