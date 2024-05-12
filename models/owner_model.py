from sqlalchemy import Column, BigInteger, String, Integer
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class OwnerModel(BaseModel):
    __tablename__ = 'owners'

    notional_code = Column(BigInteger, primary_key=True)
    hashed_password = Column(String(100))
    restaurants = relationship('RestaurantModel', backref='owner')
