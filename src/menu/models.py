import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Table
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
    Column("id", String, primary_key=True, default=str(uuid.uuid4)),
    Column("title", String),
    Column("description", String),
    Column("menu_id", Integer, ForeignKey("menus.id"))
)

dishes = Table(
    "dishes",
    metadata,
    Column("id", String, primary_key=True, default=str(uuid.uuid4)),
    Column("title", String),
    Column("description", String),
    Column("price", Integer),
    Column("submenu_id", Integer, ForeignKey("submenus.id"))
)
