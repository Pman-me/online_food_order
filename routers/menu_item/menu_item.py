from fastapi import APIRouter, Depends, Query, Path
from fastapi_pagination import Page, paginate

from auth.authenticate import owner_authenticate
from repositories.menu_item_repo import MenuItemRepository
from routers.menu_item.common import menu_item_checker
from routers.restaurant.common import owner_checker
from schemas.menu_item.menu_item_schema import MenuItemCreate, MenuItemRead

router = APIRouter(tags=['menu_item'])


@router.post('/{restaurant_id}')
def add_menu(menu: MenuItemCreate, restaurant_id: int = Path(gt=0),
             repository: MenuItemRepository = Depends(MenuItemRepository),
             owner_id: int = Depends(owner_authenticate)) -> dict:

    owner_checker(owner_id, restaurant_id, repository)

    repository.create(owner_id, restaurant_id, menu)
    return {
        'message': 'Successfully created'
    }


@router.get('/{restaurant_id}/', response_model=Page[MenuItemRead])
def get_menus(restaurant_id: int = Path(gt=0), repository: MenuItemRepository = Depends(MenuItemRepository)):
    return paginate(repository.get_menus(restaurant_id))


@router.get('/search', response_model=Page[MenuItemRead])
def search_by_menu_name(name: str = Query(min_length=2), repository: MenuItemRepository = Depends(MenuItemRepository)):
    return paginate(repository.search_by_menu_name(name))


@router.put('/{restaurant_id}')
def update(menu: MenuItemCreate, restaurant_id: int = Path(gt=0), menu_id: int = Query(gt=0),
           repository: MenuItemRepository = Depends(MenuItemRepository), owner_id: int = Depends(owner_authenticate)) -> dict:

    owner_checker(owner_id, restaurant_id, repository)
    menu_item_checker(menu_id, repository)

    repository.update(owner_id, restaurant_id, menu_id, menu)
    return {
        'message': 'Menu item Successfully updated'
    }


@router.delete('/{restaurant_id}')
def delete_menu(restaurant_id: int, menu_ids: list[int], repository: MenuItemRepository = Depends(MenuItemRepository),
                owner_id: int = Depends(owner_authenticate)):

    owner_checker(owner_id, restaurant_id, repository)

    repository.delete(restaurant_id, menu_ids)
    return {
        'message': 'Successfully removed'
    }
