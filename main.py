from fastapi import FastAPI
import uvicorn

from src.database import database, engine, metadata
from src.menu.api import menu_router

app = FastAPI(title="Restaurant API")
app.include_router(menu_router, prefix="/api/v1/menus", tags=["menu"])


@app.on_event("startup")
async def startup():
    metadata.create_all(engine)
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def read_root():
    return {"Connection": "Success"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
