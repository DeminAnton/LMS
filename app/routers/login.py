from fastapi import APIRouter, Depends, Form, HTTPException, status, Response, Request
from schemas import UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from db import db_helper
from utils.security import encode_jwt, decode_jwt, validate_password
from models import User
from crud.user import get_user_by_login
from config import settings


router = APIRouter(prefix="/login", tags=["JWT login"])

async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    db = Depends(db_helper.session_getter)
    
):
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user: User = await get_user_by_login(db, username)
    if not user:
        raise unauth_exc
    if validate_password(password, user.password):
        return user
    raise unauth_exc
            

@router.post("/in/")
async def auth_user_jwt(
    response: Response,
    user: UserLogin = Depends(validate_auth_user),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    print("------------------------------------")
    print(user)
    jwt_payload = {
        "sub": user.login,
        "username": user.login,
        "email": user.email,
        "roles": " ".join([i.name for i in user.roles])
    }
    user_token = encode_jwt(payload=jwt_payload)
    
    response.set_cookie(
        key="access_token", 
        value=user_token, 
        httponly=True, 
        max_age=settings.auth_jwt.access_token_expire_minutes * 60,
        )
    return {"AccesToken": user_token,
            "TokenType": "Cookie"
    }
    
    
    
@router.get("/protected")
async def protected_route(request: Request):
    # Read token from the cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Verify the token
    payload = decode_jwt(token)
    return {"message": f"Hello, {payload['sub']}! This is a protected route."}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}