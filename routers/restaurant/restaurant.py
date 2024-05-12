from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi_pagination import Page, paginate

from auth.authenticate import get_current_owner, owner_authenticate
from repositories.restaurant_repo import RestaurantRepository
from routers.restaurant.common import owner_checker
from schemas.restaurant.restaurant_schema import RestaurantCreate, RestaurantRead

router = APIRouter(tags=['restaurant'])


@router.post('/new', status_code=status.HTTP_204_NO_CONTENT, summary='Add new restaurant')
def add_restaurant(restaurant: RestaurantCreate, repository: RestaurantRepository = Depends(RestaurantRepository),
                   owner_id: int = Depends(owner_authenticate)):
    if repository.restaurant_exist(restaurant.name, owner_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Restaurant with supplied name exist'
        )
    repository.create_restaurant(restaurant, int(owner_id))
    return {
        'message': 'Successfully added'
    }


@router.get('/', summary='Fetch restaurant by owner\'s notional code')
def get_restaurant(repository: RestaurantRepository = Depends(RestaurantRepository), owner_id: int = Depends(owner_authenticate)):
    return repository.get_restaurant_by_owner_id(owner_id)


@router.get('/all', response_model=Page[RestaurantRead], summary='Fetch all restaurant')
def get_all_restaurants(repository: RestaurantRepository = Depends(RestaurantRepository)):
    return paginate(repository.get_all_restaurants())


@router.put('/category/{restaurant_id}')
def update_category(categories: list[str], restaurant_id: int = Path(gt=0),
                    repository: RestaurantRepository = Depends(RestaurantRepository),
                    owner_id: int = Depends(owner_authenticate)) -> dict:

    owner_checker(owner_id, restaurant_id, repository)
    repository.add_new_category(owner_id, restaurant_id, categories)
    return {
        'message': 'Category successfully updated'
    }


@router.delete('/category/{restaurant_id}')
def delete_category(category: str, restaurant_id: int = Path(gt=0),
                    repository: RestaurantRepository = Depends(RestaurantRepository),
                    owner_id: int = Depends(owner_authenticate)):

    owner_checker(owner_id, restaurant_id, repository)
    return repository.delete_category(owner_id, restaurant_id=restaurant_id, category=category)


@router.put('/{restaurant_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Update restaurant\'s data')
def update(restaurant: RestaurantCreate, restaurant_id: int = Path(gt=0),
           repository: RestaurantRepository = Depends(RestaurantRepository),
           owner_id: int = Depends(owner_authenticate)):

    owner_checker(owner_id, restaurant_id, repository)
    repository.update_restaurant(restaurant, restaurant_id, owner_id)
    return {
        'message': 'Successfully updated'
    }


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete(restaurant_id: int = Path(gt=0), repository: RestaurantRepository = Depends(RestaurantRepository),
           owner_id: int = Depends(get_current_owner)):

    owner_checker(owner_id, restaurant_id, repository)
    repository.delete_restaurant_by_id(restaurant_id)
    return {
        'message': 'Successfully removed'
    }
