import uvicorn
from fastapi import FastAPI
from routers import router as api_router
from config import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.prefix.api)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)