from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class DishBase(BaseModel):
    title: str
    description: str
    price: int


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: UUID
    submenu_id: int

    class Config:
        from_attributes = True


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    pass


class Submenu(SubmenuBase):
    id: UUID
    main_menu_id: int
    dishes: list[Dish] = []

    class Config:
        from_attributes = True


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: str
    submenus: list[Submenu] = []

    class Config:
        from_attributes = True
