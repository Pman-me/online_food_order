from sqlalchemy import select, insert, exc

from auth.hash import Hash
from repositories.base_repository import BaseRepository
from models.customer_model import CustomerModel
from schemas.customer.customer_schema import CustomerRead, CustomerCreate


class CustomersRepository(BaseRepository):
    def get_customer(self, username: str) -> CustomerRead | None:
        try:
            stmt = select(CustomerModel).where(CustomerModel.username == username)
            customer_exist = self.session.execute(stmt).scalar()
            if customer_exist is not None:
                return CustomerRead.model_validate(customer_exist)
            return None
        except exc.SQLAlchemyError as err:
            pass

    def create_customer(self, customer: CustomerCreate):
        try:
            create_query = insert(CustomerModel).values(
                username=customer.username,
                phoneNumber=customer.phone_number,
                hashed_password=Hash.create_hash(customer.password),
                creator=customer.username
            )
            self.session.execute(create_query)
            self.session.commit()
        except exc.SQLAlchemyError as err:
            pass

