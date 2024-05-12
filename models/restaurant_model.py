from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, ARRAY
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class RestaurantModel(BaseModel):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    description = Column(String(200))
    image_url = Column(String(200))
    address = Column(String(200))
    location = Column(String(20))
    categories = Column(ARRAY(String(20)))
    open_time = Column(String(8))
    close_time = Column(String(8))
    owner_id = Column(BigInteger, ForeignKey('owners.notional_code', ondelete='cascade', onupdate='cascade'))
    menu_items = relationship('MenuItemModel', backref='restaurant')
