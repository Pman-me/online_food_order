from datetime import datetime, timezone

from sqlalchemy import exc, select, insert, delete, update, and_

from repositories.base_repository import BaseRepository
from models.cart import CartModel
from models.cart_item import CartItemModel
from models.customer_model import CustomerModel

from schemas.menu_item.menu_item_schema import MenuItemCreate


class CartRepository(BaseRepository):

    def get_cart(self, customer_id: int):
        try:
            stmt = select(CartModel).where(CartModel.customer_id == customer_id)
            return self.session.execute(stmt).scalar()
        except exc.SQLAlchemyError as err:
            pass

    def create_cart(self, customer_id: int):
        try:
            stmt = insert(CartModel).values(
                customer_id=customer_id
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def get_cart_item(self, cart_item_id: int):
        try:
            stmt = select(CartItemModel).where(CartItemModel.id == cart_item_id)
            return self.session.execute(stmt).scalar()
        except exc.SQLAlchemyError as err:
            pass

    def add_to_cart(self, customer_id: int, menu_item: MenuItemCreate, quantity: int, cart_id: int):
        try:
            stmt = insert(CartItemModel).values(
                name=menu_item.name,
                description=menu_item.description,
                image_url=menu_item.image_url,
                category=menu_item.category,
                price=menu_item.price,
                discount=menu_item.discount,
                quantity=quantity,
                cart_id=cart_id,
                creator=customer_id,
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def delete_cart_item(self, menu_item_id: int):
        try:
            stmt = delete(CartItemModel).where(CartItemModel.id == menu_item_id)
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def update_cart_item(self, customer_id: int, menu_item_id: int, discount: float, quantity: int):
        try:
            stmt = update(CartItemModel).where(CartItemModel.id == menu_item_id).values(
                discount=discount,
                quantity=quantity,
                modifier=customer_id,
                modified_at=datetime.now(timezone.utc)
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

