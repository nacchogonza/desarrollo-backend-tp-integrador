# database.py (Para soporte completamente asíncrono con SQLAlchemy 2.0 y FastAPI)

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base # Mantén esta importación
from sqlalchemy.sql import func # Para timestamps automáticos, etc.

# Ruta al archivo de la base de datos SQLite
# NOTA: Para SQLite con async, se usa 'sqlite+aiosqlite:///'
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# engine: Se encarga de la comunicación con la base de datos.
# echo=True es útil para depuración, muestra las consultas SQL
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False # Cambia a True para ver las consultas SQL en la consola
)

# async_sessionmaker: Una clase para crear sesiones asíncronas de base de datos.
# expire_on_commit=False: Permite que los objetos permanezcan accesibles después de un commit.
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession # Importante: especifica la clase de sesión
)

# Base: La clase base de la que heredarán tus modelos de SQLAlchemy.
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos asíncrona en las rutas de FastAPI.
async def get_db() -> AsyncSession: # <--- El tipo de retorno es AsyncSession
    async with AsyncSessionLocal() as session:
        yield session