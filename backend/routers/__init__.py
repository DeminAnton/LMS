from fastapi import APIRouter
from routers.user import router as user_router
from routers.login import router as login_router

router = APIRouter()
router.include_router(user_router)
router.include_router(login_router)

