from datetime import datetime, timezone

from sqlalchemy import select, exc, insert, update, delete

from repositories.base_repository import BaseRepository
from models.menu_item import MenuItemModel
from schemas.menu_item.menu_item_schema import MenuItemCreate, MenuItemRead


class MenuItemRepository(BaseRepository):

    def get_menus(self, restaurant_id: int):
        try:
            stmt = select(MenuItemModel).where(MenuItemModel.restaurant_id == restaurant_id)

            return [MenuItemRead.model_validate(menu) for menu in self.session.execute(stmt).scalars().all()]
        except exc.SQLAlchemyError as err:
            pass

    def create(self, owner_id: int, restaurant_id: int, menu: MenuItemCreate):
        try:
            stmt = insert(MenuItemModel).values(
                name=menu.name,
                description=menu.description,
                price=menu.price,
                discount=menu.discount,
                category=menu.category,
                image_url=menu.image_url,
                restaurant_id=restaurant_id,
                creator=owner_id,
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def update(self, owner_id: int, restaurant_id: int, menu_id: int, menu: MenuItemCreate):
        try:
            stmt = update(MenuItemModel).where(MenuItemModel.id == menu_id,
                                               MenuItemModel.restaurant_id == restaurant_id).values(
                name=menu.name,
                description=menu.description,
                price=menu.price,
                discount=menu.discount,
                image_url=menu.image_url,
                restaurant_id=restaurant_id,
                modifier=owner_id,
                modified_at=datetime.now(timezone.utc)
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def delete(self, restaurant_id: int, menu_ids: list[int]):
        try:
            for menu_id in menu_ids:
                stmt = delete(MenuItemModel).where(MenuItemModel.restaurant_id == restaurant_id).where(
                    MenuItemModel.id == menu_id)
                self.session.execute(stmt)
                self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def search_by_menu_name(self, name: str):
        try:
            keyword = '%{}%'.format(name)
            stmt = select(MenuItemModel).where(MenuItemModel.name.like(keyword))
            return [MenuItemRead.model_validate(menu) for menu in self.session.execute(stmt).scalars().all()]
        except exc.SQLAlchemyError as err:
            pass
