from pydantic import BaseModel, Field

from schemas.cart.cart_schema import CartRead


class CustomerCreate(BaseModel):
    username: str = Field(min_length=3)
    phone_number: str = Field(min_length=11, max_length=14)
    password: str = Field(min_length=12)

    class Config:
        json_schema_extra = {
            'example': {
                'username': 'amir',
                'phone_number': '09123334455',
                'password': 'jo4!ksI0('
            }
        }


class CustomerRead(BaseModel):
    id: int
    username: str
    phone_number: str
    hashed_password: str

    class Config:
        from_attributes = True


