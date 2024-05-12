from fastapi import HTTPException, status

from repositories.cart_repo import CartRepository


def cart_exists(customer_id, repository: CartRepository) -> int:
    cart = repository.get_cart(customer_id)
    if not cart:
        repository.create_cart(customer_id)
        cart = repository.get_cart(customer_id)
    return cart.id


def customer_checker(expected_customer_id, customer_id_from_token):
    if expected_customer_id != customer_id_from_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

