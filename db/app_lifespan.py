from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.base import SQLBASE
from db.connection import engine


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # async with engine.begin() as conn:
    #     await conn.run_sync(SQLBASE.metadata.create_all)
    import models.cart
    import models.owner_model
    import models.customer_model
    import models.restaurant_model
    import models.cart_item
    import models.menu_item
    SQLBASE.metadata.create_all(bind=engine)
    yield
