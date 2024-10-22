from schemas import SessionCreate
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from models import Session, User
from datetime import datetime, timedelta
from config import settings




async def create_session(db: AsyncSession, session: SessionCreate) -> Session:
    result = await db.execute(select(User).filter(User.user_id == session.user_id))
    current_user = result.scalar()
    if not current_user:
        raise ValueError("User not found")
    new_session = Session(
        user_id=session.user_id, 
        session_key=session.session_key,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(
            hours=settings.auth_jwt.session_token_expire_hours,
            ),
        ip_address=session.ip_address,
        user_agent=session.user_agent
        )
    db.add(new_session)
    await db.commit()
    return new_session

async def get_session_by_session_token(db: AsyncSession, session_key: str) -> Session | None:
    result = await db.execute(select(Session).
                              options(joinedload(Session.user)).
                              filter(Session.session_key == session_key))
    
    session:Session = result.scalar()
    if not session:
        raise ValueError("Session not found")
    return session

async def update_session(db: AsyncSession, session_key:str, is_active:bool| None = None) -> Session | None:
    result = await db.execute(select(Session).filter(Session.session_token == session_key))
    session:Session = result.scalar()
    if not session:
        return None

    session.last_active_at = datetime.utcnow()
    if is_active:
        session.is_active = is_active

    await db.commit()
    await db.refresh(session)
    return session
