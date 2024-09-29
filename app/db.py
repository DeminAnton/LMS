from sqlalchemy import create_engine, MetaData, text
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession, create_async_engine
from config import settings


class DataBaseHelper():
    def __init__(
        self,
        url: str,
        echo: bool,
        echo_pool: bool,
        pool_size: int = 5,
        max_overflow: int = 10
        ) -> None:
        
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            )
        
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False            
        )
        
    async def dispose(self) -> None:
        await self.engine.dispose()
        
    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            
db_helper = DataBaseHelper(
    url=str(settings.db_config.db_url_async),
    echo=settings.db_config.db_echo,
    echo_pool=settings.db_config.db_echo_pool,
    pool_size=settings.db_config.pool_size,
    max_overflow=settings.db_config.max_overflow
    )


        
