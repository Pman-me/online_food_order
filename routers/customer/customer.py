from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.hash import Hash
from auth.jwt_handler import create_access_token
from repositories.customer_repo import CustomersRepository
from schemas.customer.customer_schema import CustomerCreate
from schemas.user_type import UserType

router = APIRouter(tags=['customer'])


@router.post('/signup')
def sign_user_up(user: CustomerCreate, repository: CustomersRepository = Depends(CustomersRepository)) -> dict:
    if repository.get_customer(user.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with supplied username exists'
        )
    repository.create_customer(user)
    return {'message': 'User successfully registered'}


@router.post('/signin')
def sign_user_in(user: OAuth2PasswordRequestForm = Depends(), repository: CustomersRepository = Depends(CustomersRepository)) -> dict:
    user_exist = repository.get_customer(user.username)
    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User with username does not exists'
        )
    if Hash.verify_hash(user.password, user_exist.hashed_password):
        access_token = create_access_token(user_exist.id, UserType.CUSTOMER.value)
        return {
            'access_token': access_token,
            'token_type': 'Bearer'
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid details passed'
    )








