from fastapi import HTTPException, status
from sqlalchemy import select

from repositories.base_repository import BaseRepository
from models.menu_item import MenuItemModel


def menu_item_checker(menu_item_id: int, repository: BaseRepository):
    stmt = select(MenuItemModel.id).where(MenuItemModel.id == menu_item_id)
    if repository.session.execute(stmt).scalar() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Menu not found')
