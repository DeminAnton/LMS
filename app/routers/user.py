from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db import db_helper
from crud.user import create_user, get_user, update_user, delete_user, get_user_by_nickname
from schemas import UserCreate, UserOut, UserUpdate
from models import User

router = APIRouter(prefix="/users")

# Create a new user
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(db_helper.session_getter)):
    db_user = await get_user_by_nickname(db, user.nickname)
    if db_user:
        raise HTTPException(status_code=400, detail="Nickname already registered")
    new_user = await create_user(db, user, role_name="user")  # Default to the "user" role
    return new_user

# Get user by ID
@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    db_user = await get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update a user
@router.put("/{user_id}", response_model=UserOut)
async def update_existing_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(db_helper.session_getter)):
    updated_user = await update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Delete a user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    if not await delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
