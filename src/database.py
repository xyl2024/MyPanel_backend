from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./data/mypanel.db"

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    connect_args={"check_same_thread": False},  # 允许在不同线程间共享连接
    echo=True,  # 可以设置为 False 关闭 SQL 日志
)

# 异步数据库会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 默认(True)提交事务后对象属性过期，下次访问需重新查询, False: 提交后对象仍然可用，避免不必要的数据库查询
)

# 创建 ORM 声明式基类
# 所有数据模型类都必须继承这个 Base 类
# Base 包含了 SQLAlchemy ORM 的核心功能
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
