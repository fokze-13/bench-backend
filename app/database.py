from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from app.config import settings

engine = create_async_engine(
    settings.db_url,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
