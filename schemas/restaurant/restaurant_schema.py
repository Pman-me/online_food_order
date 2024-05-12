from typing import Union, Tuple, List

from pydantic import BaseModel, Field


class RestaurantCreate(BaseModel):
    name: str = Field(min_length=1)
    description: Union[str, None] = None
    categories: List[str]
    image_url: str
    address: str
    location: Union[Tuple[float, float], None] = None
    open_time: Union[str, None] = None
    close_time: Union[str, None] = None


class RestaurantRead(BaseModel):
    id: int
    name: str
    description: str
    categories: List[str]
    image_url: str
    address: str
    location: Union[Tuple[float, float], None]
    open_time: Union[str, None] = None
    close_time: Union[str, None] = None

    class Config:
        from_attributes = True
