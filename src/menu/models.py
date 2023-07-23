from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from src.database import metadata


menus = Table(
    "menus",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("title", String, unique=True)
)

submenus = Table(
    "submenus",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("title", String, unique=True),
    Column("menu_id", Integer, ForeignKey("menus.id"))
)

dishes = Table(
    "dishes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("title", String, unique=True),
    Column("price", Integer),
    Column("submenu_id", Integer, ForeignKey("submenus.id"))
)
