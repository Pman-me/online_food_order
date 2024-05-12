from sqlalchemy import Column, Integer, ForeignKey, String, Float

from models.base_model import BaseModel


class CartItemModel(BaseModel):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String())
    description = Column(String())
    price = Column(Integer, nullable=False, default=0)
    quantity = Column(Integer, nullable=False, default=1)
    discount = Column(Float)
    image_url = Column(String())
    category = Column(String())
    cart_id = Column(Integer, ForeignKey('carts.id', ondelete='cascade', onupdate='cascade'))
    menu_item_id = Column(Integer, ForeignKey('menu_items.id', ondelete='cascade', onupdate='cascade'))
