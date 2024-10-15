from schemas import SessionCreate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from models import Session, User




async def create_session(db: AsyncSession, session: SessionCreate) -> Session:
    result = await db.execute(select(User).filter(User.user_id == session.user_id))
    current_user = result.scalar()
    if not current_user:
        raise ValueError("User not found")
    new_session = Session(
        user_id=session.user_id, 
        session_token=session.session_token,
        created_at=session.created_at,
        expires_at=session.expires_at,
        ip_address=session.ip_address,
        user_agent=session.user_agent
        )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session
