from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    price: int


class Dish(DishBase):
    id: int
    submenu_id: int

    class Config:
        from_attributes = True


class SubmenuBase(BaseModel):
    title: str


class Submenu(SubmenuBase):
    id: int
    main_menu_id: int
    dishes: list[Dish] = []

    class Config:
        from_attributes = True


class MenuBase(BaseModel):
    title: str


class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: int
    submenus: list[Submenu] = []

    class Config:
        from_attributes = True
