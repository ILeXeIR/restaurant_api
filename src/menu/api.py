import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select
from typing import List

from src.database import database
from .models import menus, submenus, dishes
from .schemas import Menu, MenuCreate, MenuExtra, \
                    Submenu, SubmenuCreate, SubmenuExtra, \
                    Dish, DishCreate


menu_router = APIRouter()


@menu_router.get("/{menu_id}", response_model=MenuExtra)
async def get_menu(menu_id: str):
    query = menus.select().where(menus.c.id == menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    join_query = submenus.join(dishes, submenus.c.id == dishes.c.submenu_id,
                               isouter=True)
    query = select([
            func.count(func.distinct(submenus.c.id)).label("submenus_count"),
            func.count(dishes.c.id).label("dishes_count")
        ]).select_from(join_query).where(submenus.c.menu_id == menu_id)
    result = await database.fetch_one(query)
    values = dict(db_menu)
    values["submenus_count"] = result["submenus_count"]
    values["dishes_count"] = result["dishes_count"]
    return MenuExtra.parse_obj(values)


@menu_router.get("/", response_model=List[Menu])
async def get_menus(skip: int = 0, limit: int = 100):
    query = menus.select().limit(limit).offset(skip)
    return await database.fetch_all(query)


@menu_router.post("/", status_code=201, response_model=Menu)
async def create_menu(menu: MenuCreate):
    values = menu.dict()
    values["id"] = str(uuid.uuid4())
    query = menus.insert().values(**values)
    await database.execute(query)
    return Menu.parse_obj({**values})


@menu_router.get("/all/submenus", response_model=List[Submenu])
async def get_all_submenus():
    query = submenus.select()
    return await database.fetch_all(query)


@menu_router.get("/all/dishes", response_model=List[Dish])
async def get_all_dishes():
    query = dishes.select()
    return await database.fetch_all(query)


@menu_router.patch("/{menu_id}", response_model=Menu)
async def update_menu(menu_id: str, menu: MenuCreate):
    query = menus.select().where(menus.c.id == menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    query = menus.update().where(menus.c.id == db_menu.id).values(**menu.dict())
    await database.execute(query=query)
    return Menu.parse_obj({**menu.dict(), "id": db_menu.id})


@menu_router.delete("/{menu_id}")
async def delete_menu(menu_id: str) -> dict:
    query = menus.select().where(menus.c.id == menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    query = menus.delete().where(menus.c.id == db_menu.id)
    await database.execute(query=query)
    return {"status": True}


@menu_router.get("/{menu_id}/submenus/{submenu_id}",
                 response_model=SubmenuExtra)
async def get_submenu(menu_id: str, submenu_id: str):
    query = submenus.select().where(submenus.c.id == submenu_id,
                                    submenus.c.menu_id == menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    query = select([func.count()]).select_from(dishes).where(
        dishes.c.submenu_id == submenu_id)
    dishes_count = await database.fetch_val(query)
    return SubmenuExtra.parse_obj({**db_submenu, "dishes_count": dishes_count})


@menu_router.get("/{menu_id}/submenus", response_model=List[Submenu])
async def get_submenus(menu_id: str):
    query = menus.select().where(menus.c.id == menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    query = submenus.select().where(submenus.c.menu_id == menu_id)
    return await database.fetch_all(query)


@menu_router.post("/{menu_id}/submenus", status_code=201,
                  response_model=Submenu)
async def create_submenu(submenu: SubmenuCreate, menu_id: str):
    values = submenu.dict()
    values["id"] = str(uuid.uuid4())
    values["menu_id"] = menu_id
    query = submenus.insert().values(**values)
    await database.execute(query)
    return Submenu.parse_obj({**values})


@menu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=Submenu)
async def update_submenu(menu_id: str, submenu_id: str, submenu: SubmenuCreate):
    query = submenus.select().where(submenus.c.id == submenu_id,
                                    submenus.c.menu_id == menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    query = submenus.update().where(submenus.c.id == db_submenu.id).values(
        **submenu.dict())
    await database.execute(query=query)
    result = {**submenu.dict(), "id": submenu_id, "menu_id": menu_id}
    return Submenu.parse_obj(result)


@menu_router.delete("/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: str, submenu_id: str) -> dict:
    query = submenus.select().where(submenus.c.id == submenu_id,
                                    submenus.c.menu_id == menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    query = submenus.delete().where(submenus.c.id == db_submenu.id)
    await database.execute(query=query)
    return {"status": True}


@menu_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                 response_model=Dish)
async def get_dish(menu_id: str, submenu_id: str, dish_id: str):
    query = dishes.select().where(dishes.c.id == dish_id,
                                  dishes.c.submenu_id == submenu_id)
    db_dish = await database.fetch_one(query)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    query = submenus.select().where(submenus.c.id == submenu_id,
                                    submenus.c.menu_id == menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return Dish.parse_obj(db_dish)


@menu_router.get("/{menu_id}/submenus/{submenu_id}/dishes",
                 response_model=List[Dish])
async def get_dishes(menu_id: str, submenu_id: str):
    query = submenus.select().where(submenus.c.id == submenu_id,
                                    submenus.c.menu_id == menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        return []
        # raise HTTPException(status_code=404, detail="submenu not found")
    query = dishes.select().where(dishes.c.submenu_id == submenu_id)
    return await database.fetch_all(query)


@menu_router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=201,
                  response_model=Dish)
async def create_dish(dish: DishCreate, menu_id: str, submenu_id: str):
    query = submenus.select().where(submenus.c.id == submenu_id,
                                    submenus.c.menu_id == menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    values = dish.dict()
    values["price"] = "{:.2f}".format(dish.price)
    values["id"] = str(uuid.uuid4())
    values["submenu_id"] = submenu_id
    query = dishes.insert().values(**values)
    await database.execute(query)
    return Dish.parse_obj({**values})


@menu_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                   response_model=Dish)
async def update_dish(menu_id: str, submenu_id: str, dish_id: str,
                      dish: DishCreate):
    query = dishes.select().where(dishes.c.id == dish_id,
                                  dishes.c.submenu_id == submenu_id)
    db_dish = await database.fetch_one(query)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    query = submenus.select().where(submenus.c.id == submenu_id,
                                    submenus.c.menu_id == menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    values = dish.dict()
    values["price"] = "{:.2f}".format(dish.price)
    query = dishes.update().where(dishes.c.id == db_dish.id).values(values)
    await database.execute(query=query)
    values["id"] = dish_id
    values["submenu_id"] = submenu_id
    return Dish.parse_obj(values)


@menu_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(menu_id: str, submenu_id: str, dish_id: str) -> dict:
    query = dishes.select().where(dishes.c.id == dish_id,
                                  dishes.c.submenu_id == submenu_id)
    db_dish = await database.fetch_one(query)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    query = submenus.select().where(submenus.c.id == submenu_id,
                                    submenus.c.menu_id == menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    query = dishes.delete().where(dishes.c.id == db_dish.id)
    await database.execute(query=query)
    return {"status": True}
