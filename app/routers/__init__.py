from fastapi import APIRouter
from routers.user import router as user_router

router = APIRouter()
router.include_router(user_router)
