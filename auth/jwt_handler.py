import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import jwt, JWTError

from schemas.user_type import UserType
from settings import Settings


def create_access_token(id: int, type: UserType):
    pay_load = {
        'id': id,
        'type': type,
        'expires': time.time() + 3600
    }
    return jwt.encode(pay_load, Settings().SECRET_KEY, algorithm='HS256')


def verify_access_token(token: str):
    payload = jwt.decode(token, Settings().SECRET_KEY, algorithms='HS256')
    expire = payload.get('expires')
    try:
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No access token supplied'
            )

        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Token expired'
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid token'
        )
