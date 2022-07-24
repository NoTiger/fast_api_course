import uvicorn
from fastapi import FastAPI

from db.database import engine
from db import db_schema
from routers import item as item_router


app = FastAPI()

db_schema.Base.metadata.create_all(bind=engine)

app.include_router(item_router.router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
