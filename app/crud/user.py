from schemas import UserCreate, UserOut, UserUpdate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from models import User, Role


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def create_user(db: AsyncSession, user: UserCreate, role_name: str) -> User:
    result = await db.execute(select(Role).filter(Role.name == role_name))
    role = result.scalar()
    if not role:
        raise ValueError("Role not found")

    hashed_password = hash_password(user.password)
    db_user = User(nickname=user.nickname, email=user.email, password=hashed_password, role_id=role.id)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Get user by ID
async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar()

# Get user by nickname
async def get_user_by_nickname(db: AsyncSession, nickname: str) -> User | None:
    result = await db.execute(select(User).filter(User.nickname == nickname))
    return result.scalar()

# Update user information
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User | None:
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar()
    if not db_user:
        return None

    if user_update.nickname:
        db_user.nickname = user_update.nickname
    if user_update.email:
        db_user.email = user_update.email

    await db.commit()
    await db.refresh(db_user)
    return db_user

# Delete a user
async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar()
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False