from pydantic import Field, BaseModel

from schemas.restaurant.restaurant_schema import RestaurantRead


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str
    price: int
    discount: float
    category: str
    image_url: str


class MenuItemRead(BaseModel):
    id: int
    name: str = Field(min_length=2)
    description: str
    price: str | int
    discount: float
    category: str
    image_url: str
    restaurant: RestaurantRead

    class Config:
        from_attributes = True
