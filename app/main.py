import uvicorn
from fastapi import FastAPI
from routers import router as api_router
from config import settings
from db import db_helper
from contextlib import asynccontextmanager
from models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    yield
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(api_router, prefix=settings.prefix.api)

if __name__ == "__main__":
    uvicorn.run("main:main_app", reload=True)
