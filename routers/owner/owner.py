from fastapi import APIRouter, Depends, HTTPException, status, Path

from auth.authenticate import get_current_owner, owner_authenticate
from auth.hash import Hash
from auth.jwt_handler import create_access_token
from repositories.owner_repo import OwnersRepository
from schemas.owner.owner_schema import OwnerIn
from schemas.user_type import UserType

router = APIRouter(tags=['owner'])


@router.post('/signup')
def sign_owner_up(owner: OwnerIn, repository: OwnersRepository = Depends(OwnersRepository)) -> dict:
    if repository.get(owner.notional_code) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Owner with supplied notional code exist'
        )
    repository.create(owner)
    return {
        'message': 'Successfully registered'
    }


@router.post('/signin')
def sign_owner_in(owner: OwnerIn, repository: OwnersRepository = Depends(OwnersRepository)) -> dict:
    owner_exist = repository.get(owner.notional_code)
    if owner_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Owner with notional code does not exist'
        )
    if Hash.verify_hash(owner.password, owner_exist.hashed_password):
        access_token = create_access_token(owner_exist.notional_code, UserType.OWNER.value)
        return {
            'access_token': access_token,
            'token_type': 'Bearer'
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid details passed'
    )


@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
def update_password(owner: OwnerIn, repository: OwnersRepository = Depends(OwnersRepository), owner_id: int = Depends(owner_authenticate)):
    repository.update(owner)
    return {
        'message': 'Password Successfully updated'
    }


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(repository: OwnersRepository = Depends(OwnersRepository), owner_id: int = Depends(owner_authenticate)):
    repository.delete(owner_id)
    return {
        'message': 'Owner Successfully removed'
    }
