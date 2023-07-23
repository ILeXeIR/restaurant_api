from fastapi import APIRouter, HTTPException
from typing import List

from src.database import database
from .models import menus, submenus, dishes
from .schemas import Menu, MenuCreate


menu_router = APIRouter()


@menu_router.get("/{menu_id}", response_model=Menu)
async def get_menu(menu_id: int):
    query = menus.select().where(menus.c.id==menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return Menu.parse_obj(db_menu)


@menu_router.get("/", response_model=List[Menu])
async def get_menus(skip: int = 0, limit: int = 100):
    query = menus.select().limit(limit).offset(skip)
    return await database.fetch_all(query)


@menu_router.post("/", response_model=Menu)
async def create_menu(menu: MenuCreate):
    query = menus.insert().values(title=menu.title)
    id = await database.execute(query)
    return Menu.parse_obj({**menu.dict(), "id": id})

@menu_router.put("/{menu_id}", response_model=Menu)
async def update_menu(menu_id: int, menu: MenuCreate):
    query = menus.select().where(menus.c.id==menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    query = menus.update().where(menus.c.id==db_menu.id).values(**menu.dict())
    await database.execute(query=query)
    return Menu.parse_obj({**menu.dict(), "id": db_menu.id})

@menu_router.delete("/{menu_id}")
async def delete_menu(menu_id: int) -> dict:
    query = menus.select().where(menus.c.id==menu_id)
    db_menu = await database.fetch_one(query)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    query = menus.delete().where(menus.c.id==db_menu.id)
    await database.execute(query=query)
    return {"status": True}
