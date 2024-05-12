from fastapi import APIRouter, Depends, Path, Query

from auth.authenticate import customer_authenticate
from repositories.cart_repo import CartRepository
from routers.cart.common import cart_exists, customer_checker
from schemas.menu_item.menu_item_schema import MenuItemCreate

router = APIRouter(tags=['cart'])


@router.post('/add/{customer_id}')
def add_to_cart(menu_item: MenuItemCreate, customer_id: int = Path(gt=0), quantity: int = Query(gt=0),
                repository: CartRepository = Depends(CartRepository),
                customer_id_from_token: int = Depends(customer_authenticate)) -> dict:
    customer_checker(customer_id, customer_id_from_token)
    cart_id = cart_exists(customer_id_from_token, repository)

    repository.add_to_cart(customer_id_from_token, menu_item, quantity, cart_id)
    return {
        'message': 'Successfully added to cart'
    }


@router.delete('/remove/{customer_id}')
def remove_from_cart(customer_id: int = Path(gt=0), cart_item_id: int = Query(gt=0),
                     repository: CartRepository = Depends(CartRepository),
                     customer_id_from_token: int = Depends(customer_authenticate)):
    customer_checker(customer_id, customer_id_from_token)
    cart_exists(customer_id_from_token, repository)

    repository.delete_cart_item(cart_item_id)
    return {
        'message': 'Successfully removed from cart'
    }


@router.put('/update/{customer_id}')
def update_cart_item(customer_id: int = Path(gt=0), cart_item_id: int = Query(gt=0), discount: float = Query(gt=0),
                     quantity: int = Query(gt=0),
                     repository: CartRepository = Depends(CartRepository),
                     customer_id_from_token: int = Depends(customer_authenticate)):
    customer_checker(customer_id, customer_id_from_token)
    cart_exists(customer_id_from_token, repository)

    repository.update_cart_item(customer_id_from_token, cart_item_id, discount, quantity)
    return {
        'message': 'Successfully cart updated'
    }
