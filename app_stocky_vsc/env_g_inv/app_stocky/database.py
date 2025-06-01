from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL="sqlite+aiosqlite:///./database.db"
engine=create_async_engine(DATABASE_URL,echo=True)
AsyncSessionAsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
bind=engine
class_=AsyncSession
expire_on_commit=False
Base=declarative_base()
Target_metadata=Base.metadata
