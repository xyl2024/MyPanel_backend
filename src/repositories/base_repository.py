from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# 类型变量T 代表任意的 ORM model 类, 就是 src/models/ 目录下的那些数据库模型
# 后续 BaseRepository[T] 就表示针对类型T的一个仓储类
# 例如 BaseRepository[Todo] 就用于操作 todo 表
T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    # 这个就是根据id字段获取表中的一行(row)记录, 一个model对象就表示一行
    # 调用这个函数, 意味着这个表中必须要有 id 字段, 如果没有, 建议对应子类重写这个函数
    async def get_by_id(self, id: int) -> Optional[T]:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        # result是一个SQLAlchemy封装的Result对象, 保存了查询到的结果集.
        # 提供多个提取结果的方法, 例如 scalar_one_or_none, scalars, scalar_one 等
        # 这里 scalar_one_or_none 表示查询到恰好一行则返回该行的model, 查到0行返回None, 查到多于1行抛出MultipleResultsFound异常
        return result.scalar_one_or_none()

    # 分页查询
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def delete(self, instance: T) -> None:
        await self.db.delete(instance)
        await self.db.commit()

    async def delete_by_id(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if instance:
            await self.delete(instance)
            return True
        return False
