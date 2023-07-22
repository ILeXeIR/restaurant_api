from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .deps import get_db
from . import models, schemas


menu_router = APIRouter()


@menu_router.get("/{menu_id}", response_model=schemas.Menu)
async def get_menu(menu_id: int, db: Session = Depends(get_db)) -> models.Menu:
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_menu


@menu_router.get("/", response_model=List[schemas.Menu])
async def get_menus(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[models.Menu]:
    return db.query(models.Menu).offset(skip).limit(limit).all()


@menu_router.post("/", response_model=schemas.Menu)
async def create_menu(
    menu: schemas.MenuCreate, db: Session = Depends(get_db)
) -> models.Menu:
    db_menu = models.Menu(title=menu.title)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu