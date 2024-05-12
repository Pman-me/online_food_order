from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from auth.jwt_handler import verify_access_token
from repositories.owner_repo import OwnersRepository

owner_oauth2_schema = OAuth2PasswordBearer(tokenUrl='/owner/signin')
customer_oauth2_schema = OAuth2PasswordBearer(tokenUrl='/customer/signin')


def owner_authenticate(token: str = Depends(owner_oauth2_schema)) -> int:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Sign in for access'
        )

    decoded_token = verify_access_token(token)
    return decoded_token['id']


def customer_authenticate(token: str = Depends(customer_oauth2_schema)) -> int:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Sign in for access'
        )
    decoded_token = verify_access_token(token)
    return decoded_token['id']


def get_current_owner(owner_notional_code: int, notional_code: str = Depends(owner_authenticate)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if notional_code is None:
        raise credentials_exception
    if owner_notional_code != int(notional_code):
        raise credentials_exception
    return notional_code
