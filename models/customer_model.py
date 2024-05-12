from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class CustomerModel(BaseModel):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    phone_number = Column(String(14))
    hashed_password = Column(String(100))
    carts = relationship('CartModel', backref='customer')
