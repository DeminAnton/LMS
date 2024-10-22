from fastapi import APIRouter, Depends, Form, HTTPException, status, Response, Request
from schemas import UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from db import db_helper
from utils.security import encode_jwt, decode_jwt, validate_password
from models import User, Session
from crud.user import get_user_by_login
from crud.session import create_session, get_session_by_session_token
from schemas import SessionCreate
from config import settings
from uuid import uuid4

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
    request: Request,
    user: UserLogin = Depends(validate_auth_user),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    new_session = SessionCreate(
        user_id=user.user_id,
        session_key=uuid4(),
        ip_address=request.client.host,
        user_agent=request.headers.get('user-agent')   
    )
    new_session:Session = create_session(db, new_session)
    
    jwt_payload = {
        "sub": new_session.session_key,
    }
    refresh_token = encode_jwt(payload=jwt_payload)
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.auth_jwt.session_token_expire_hours * 3600,
        )
    return {"RefreshToken": refresh_token,
            "TokenType": "Cookie"
    }
   
   
async def get_user_by_refresh_token(request: Request, db=Depends(db_helper.session_getter))-> User:
    token = request.cookies.get("RefreshToken")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_jwt(token)
    session = await get_session_by_session_token(db, payload['sub'])
    user = session.user
    return user

@router.post("/refresh")
async def refresh_token(db=Depends(db_helper.session_getter)):
    user = get_user_by_refresh_token()
    if not user:
        raise HTTPException(status_code=401, detail="Refresh token expired, please log in again.")
    

    
    
    
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
    response.delete_cookie(key="RefreshToken")
    return {"message": "Logout successful"}
