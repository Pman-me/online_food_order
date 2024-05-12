from pydantic import BaseModel


class CartRead(BaseModel):
    total_price: float
