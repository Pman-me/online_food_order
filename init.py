from fastapi import FastAPI
from fastapi_pagination import add_pagination

from db.app_lifespan import app_lifespan
from routers.cart import cart
from routers.menu_item import menu_item
from routers.customer import customer
from routers.owner import owner
from routers.restaurant import restaurant


app = FastAPI(lifespan=app_lifespan)
add_pagination(app)


app.include_router(prefix='/customer', router=customer.router)
app.include_router(prefix='/owner', router=owner.router)
app.include_router(prefix='/restaurant', router=restaurant.router)
app.include_router(prefix='/menu_item', router=menu_item.router)
app.include_router(prefix='/cart', router=cart.router)
