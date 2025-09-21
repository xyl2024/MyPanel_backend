from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from src.database import engine, Base
from src.routers import todo


# 创建所有表，如果表已存在则不重复创建
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 应用生命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行的代码
    await init_db()
    print("数据库表已创建")

    yield  # 应用运行期间

    # 关闭时执行的代码（如果需要）
    print("应用正在关闭")
    # 可以在这里添加清理代码，比如关闭数据库连接等


app = FastAPI(title="MyPanel后端API", lifespan=lifespan)

app.include_router(todo.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the MyPanel backend API"}
