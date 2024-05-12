from datetime import datetime, timezone

from sqlalchemy import exc, literal
from sqlalchemy import select, insert, update, delete, func

from repositories.base_repository import BaseRepository
from models.restaurant_model import RestaurantModel
from schemas.restaurant.restaurant_schema import RestaurantCreate, RestaurantRead


class RestaurantRepository(BaseRepository):

    def restaurant_exist(self, name: str, owner_id: int):
        restaurant_exist = (self.session.execute(
            select(RestaurantModel).where(RestaurantModel.name == name)).scalar())
        if restaurant_exist:

            if restaurant_exist.owner_id == owner_id:
                return None
            else:
                return RestaurantRead.model_validate(restaurant_exist)

        return None

    def get_restaurant_by_owner_id(self, owner_id: int):
        return [RestaurantRead.model_validate(rest) for rest in self.session.execute(
            select(RestaurantModel).where(RestaurantModel.owner_id == owner_id)).scalars().all()]

    def get_all_restaurants(self):
        return [RestaurantRead.model_validate(rest) for rest in
                self.session.execute(select(RestaurantModel)).scalars().all()]

    def add_new_category(self, owner_id: int, restaurant_id: int, categories: list[str]):
        try:
            stmt = update(RestaurantModel).where(RestaurantModel.id == restaurant_id).values(
                categories=func.array_cat(RestaurantModel.categories, categories),
                modifier=owner_id,
                modified_at=datetime.now(timezone.utc)
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def delete_category(self, owner_id: int, *, restaurant_id: int, category: str):
        try:
            stmt = update(RestaurantModel).where(RestaurantModel.id == restaurant_id).values(
                categories=func.array_remove(RestaurantModel.categories, literal(category)),
                modifier=owner_id,
                modified_at=datetime.now(timezone.utc)
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def create_restaurant(self, rest: RestaurantCreate, owner_id: int):
        try:
            stmt = insert(RestaurantModel).values(
                name=rest.name,
                description=rest.description,
                categories=rest.categories,
                image_url=rest.image_url,
                address=rest.address,
                location=rest.location,
                open_time=rest.open_time,
                close_time=rest.close_time,
                owner_id=owner_id,
                creator=owner_id,
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def update_restaurant(self, restaurant: RestaurantCreate, restaurant_id: int, owner_id: int):
        try:
            stmt = update(RestaurantModel).where(RestaurantModel.id == restaurant_id).values(
                name=restaurant.name,
                description=restaurant.description,
                categories=func.array_replace(RestaurantModel.categories, RestaurantModel.categories,
                                              literal(restaurant.categories)),
                image_url=restaurant.image_url,
                address=restaurant.address,
                location=restaurant.location,
                open_time=restaurant.open_time,
                close_time=restaurant.close_time,
                modifier=owner_id,
                modified_at=datetime.now(timezone.utc)
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def delete_restaurant_by_id(self, restaurant_id: int):
        try:
            stmt = delete(RestaurantModel).where(RestaurantModel.id == restaurant_id)
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def search_by_restaurant_name(self, name: str):
        pass
