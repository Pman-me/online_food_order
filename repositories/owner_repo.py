from sqlalchemy import select, insert, update, exc, delete, DateTime
from datetime import datetime, timezone

from auth.hash import Hash
from repositories.base_repository import BaseRepository
from models.owner_model import OwnerModel
from schemas.owner.owner_schema import OwnerIn, OwnerRead


class OwnersRepository(BaseRepository):

    def get(self, notional_code: int) -> OwnerRead | None:
        stmt = select(OwnerModel).where(OwnerModel.notional_code == notional_code)
        owner_exist = self.session.execute(stmt).scalar()
        if owner_exist is not None:
            return OwnerRead.model_validate(owner_exist)
        return None

    def create(self, owner: OwnerIn):
        try:
            create_query = insert(OwnerModel).values(
                notional_code=owner.notional_code,
                hashed_password=Hash.create_hash(owner.password),
                creator=owner.notional_code,
            )
            self.session.execute(create_query)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def update(self, owner: OwnerIn):
        try:
            stmt = update(OwnerModel).where(OwnerModel.notional_code == owner.notional_code).values(
                notional_code=owner.notional_code,
                hashed_password=Hash.create_hash(owner.password),
                modifier=owner.notional_code,
                modified_at=DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
            )
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

    def delete(self, owner_id: int):
        try:
            stmt = delete(OwnerModel).where(OwnerModel.notional_code == owner_id)
            self.session.execute(stmt)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            print(err)
            pass

