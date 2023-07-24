import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select
from typing import List

from src.database import database
from .models import menus, submenus
from .schemas import (Menu, MenuCreate, MenuExtra,
                    Submenu, SubmenuCreate, SubmenuExtra)


menu_router = APIRouter()


@menu_router.get("/{menu_id}", response_model=MenuExtra)
async def get_menu(menu_id: str):
    query = menus.select().where(menus.c.id==menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    query = select([func.count()]).select_from(submenus).where(submenus.c.menu_id == menu_id)
    num_sub = await database.fetch_val(query)
    return MenuExtra.parse_obj({**db_menu, "submenus": num_sub})


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


@menu_router.patch("/{menu_id}", response_model=Menu)
async def update_menu(menu_id: str, menu: MenuCreate):
    query = menus.select().where(menus.c.id==menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    query = menus.update().where(menus.c.id==db_menu.id).values(**menu.dict())
    await database.execute(query=query)
    return Menu.parse_obj({**menu.dict(), "id": db_menu.id})


@menu_router.delete("/{menu_id}")
async def delete_menu(menu_id: str) -> dict:
    query = menus.select().where(menus.c.id==menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    query = menus.delete().where(menus.c.id==db_menu.id)
    await database.execute(query=query)
    return {"status": True}


@menu_router.get("/{menu_id}/submenus/{submenu_id}",
                response_model=SubmenuExtra)
async def get_submenu(menu_id: str, submenu_id: str):
    query = submenus.select().where(submenus.c.id==submenu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None or db_submenu.menu_id != menu_id:
        raise HTTPException(status_code=404, detail="submenu not found")
    return Submenu.parse_obj(db_submenu)


@menu_router.get("/{menu_id}/submenus", response_model=List[Submenu])
async def get_submenus(menu_id: str):
    query = submenus.select().where(submenus.c.menu_id==menu_id)
    return await database.fetch_all(query)


@menu_router.post("/{menu_id}/submenus", status_code=201, response_model=Submenu)
async def create_submenu(submenu: SubmenuCreate, menu_id: str):
    values = submenu.dict()
    values["id"] = str(uuid.uuid4())
    values["menu_id"] = menu_id
    query = submenus.insert().values(**values)
    await database.execute(query)
    return Submenu.parse_obj({**values})


@menu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=Submenu)
async def update_submenu(menu_id: str, submenu_id: str, submenu: SubmenuCreate):
    query = submenus.select().where(submenus.c.id==submenu_id,
                                    submenus.c.menu_id==menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    query = submenus.update().where(submenus.c.id==db_submenu.id).values(**submenu.dict())
    await database.execute(query=query)
    result = {**submenu.dict(), "id": submenu_id, "menu_id": menu_id}
    return Submenu.parse_obj(result)


@menu_router.delete("/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: str, submenu_id: str) -> dict:
    query = submenus.select().where(submenus.c.id==submenu_id,
                                    submenus.c.menu_id==menu_id)
    db_submenu = await database.fetch_one(query)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    query = submenus.delete().where(submenus.c.id==db_submenu.id)
    await database.execute(query=query)
    return {"status": True}




# @menu_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
#                     response_model=Dish)
# async def get_dish(menu_id: str, submenu_id: str):
#     query = submenus.select().where(submenus.c.id==submenu_id)
#     db_submenu = await database.fetch_one(query)
#     if db_submenu is None or db_submenu.menu_id != menu_id:
#         raise HTTPException(status_code=404, detail="submenu not found")
#     return Submenu.parse_obj(db_submenu)


# @menu_router.get("/{menu_id}/submenus", response_model=List[Submenu])
# async def get_dishes(menu_id: str):
#     query = submenus.select().where(submenus.c.menu_id==menu_id)
#     return await database.fetch_all(query)


# @menu_router.post("/{menu_id}/submenus", status_code=201, response_model=Submenu)
# async def create_dish(submenu: SubmenuCreate, menu_id: str):
#     values = submenu.dict()
#     values["id"] = str(uuid.uuid4())
#     values["menu_id"] = menu_id
#     query = submenus.insert().values(**values)
#     await database.execute(query)
#     return Submenu.parse_obj({**values})


# @menu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=Submenu)
# async def update_dish(menu_id: str, submenu_id: str, submenu: SubmenuCreate):
#     query = submenus.select().where(submenus.c.id==submenu_id,
#                                     submenus.c.menu_id==menu_id)
#     db_submenu = await database.fetch_one(query)
#     if db_submenu is None:
#         raise HTTPException(status_code=404, detail="submenu not found")
#     query = submenus.update().where(submenus.c.id==db_submenu.id).values(**submenu.dict())
#     await database.execute(query=query)
#     result = {**submenu.dict(), "id": submenu_id, "menu_id": menu_id}
#     return Submenu.parse_obj(result)


# @menu_router.delete("/{menu_id}/submenus/{submenu_id}")
# async def delete_dish(menu_id: str, submenu_id: str) -> dict:
#     query = submenus.select().where(submenus.c.id==submenu_id,
#                                     submenus.c.menu_id==menu_id)
#     db_submenu = await database.fetch_one(query)
#     if db_submenu is None:
#         raise HTTPException(status_code=404, detail="submenu not found")
#     query = submenus.delete().where(submenus.c.id==db_submenu.id)
#     await database.execute(query=query)
#     return {"status": True}