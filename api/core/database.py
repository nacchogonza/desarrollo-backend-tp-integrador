from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from api.core.config import settings
import logging


logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

"""DATABASE_URL = "sqlite+aiosqlite:///./database.db" lo pasé a config.py configuración centralizada y fácil de actualizar."""
DATABASE_URL = settings.DATABASE_URL
logger.info(f"Usando URL de base de datos: {DATABASE_URL}")

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()
target_metadata = Base.metadata

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()