from fastapi import FastAPI
import uvicorn

from src.database import engine
from src.menu import models
from src.menu.api import menu_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant API")
app.include_router(menu_router, prefix="/menu", tags=["menu"])

@app.get("/")
async def read_root():
    return {"Connection": "Success"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
