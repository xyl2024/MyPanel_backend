from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./data/mypanel.db"

engine = create_async_engine(
    ASYNC_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True  # 可以设置为 False 关闭 SQL 日志
)

AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session