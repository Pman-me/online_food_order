from fastapi import HTTPException, status
from sqlalchemy import select

from repositories.base_repository import BaseRepository
from models.restaurant_model import RestaurantModel


def owner_checker(owner_id: int, restaurant_id: int, repository: BaseRepository):

    stmt = select(RestaurantModel.owner_id).where(RestaurantModel.id == restaurant_id,
                                                  RestaurantModel.owner_id == owner_id)

    if repository.session.execute(stmt).scalar() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
