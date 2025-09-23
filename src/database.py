# 使用 SQLAlchemy 2.0+ 的异步ORM
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 使用sqlite, aiosqlite支持异步, 若想要高并发，后续可以改为pgsql
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./data/mypanel.db"

# 创建异步数据库引擎
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    connect_args={"check_same_thread": False},  # 允许SQLite在不同线程间共享连接, 如果是pgsql则不要加这个
    echo=True,  # 打印所有执行的 SQL 语句到控制台
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


# fastapi的依赖注入函数, 用于给router函数传参使用数据库session, 具体原理看官方文档
# 它传出一个 AsyncSession (异步数据库会话)对象
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
