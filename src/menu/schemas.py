from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: str
    submenu_id: str
    price: str

    class Config:
        from_attributes = True


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    pass


class Submenu(SubmenuBase):
    id: str
    menu_id: str

    class Config:
        from_attributes = True


class SubmenuExtra(Submenu):
    dishes_count: int = 0


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: str

    class Config:
        from_attributes = True


class MenuExtra(Menu):
    submenus_count: int = 0
    dishes_count: int = 0
