import uuid

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from src.database import metadata


menus = Table(
    "menus",
    metadata,
    Column("id", String, primary_key=True),
    Column("title", String),
    Column("description", String)
)

submenus = Table(
    "submenus",
    metadata,
    Column("id", String, primary_key=True),
    Column("title", String),
    Column("description", String),
    Column("menu_id", String, ForeignKey("menus.id", ondelete='CASCADE'))
)

dishes = Table(
    "dishes",
    metadata,
    Column("id", String, primary_key=True),
    Column("title", String),
    Column("description", String),
    Column("price", String),
    Column("submenu_id", String, ForeignKey("submenus.id", ondelete='CASCADE'))
)
