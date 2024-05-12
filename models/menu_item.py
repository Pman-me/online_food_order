from sqlalchemy import Column, Integer, String, ForeignKey, Float

from models.base_model import BaseModel


class MenuItemModel(BaseModel):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    description = Column(String(100))
    price = Column(Integer)
    discount = Column(Float)
    category = Column(String(20))
    image_url = Column(String(200))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id', ondelete='cascade', onupdate='cascade'))
