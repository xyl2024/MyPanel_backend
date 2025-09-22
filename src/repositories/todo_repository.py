from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload  # 改为 selectinload
from src.models.todo import Todo
from src.repositories.base_repository import BaseRepository


class TodoRepository(BaseRepository[Todo]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Todo)

    async def get_by_id_with_tag(self, id: int) -> Optional[Todo]:
        result = await self.db.execute(
            select(Todo)
            .where(Todo.id == id)
            .options(selectinload(Todo.tag))  # 使用 selectinload
        )
        return result.scalar_one_or_none()

    async def get_all_with_tags(self, skip: int = 0, limit: int = 100) -> List[Todo]:
        result = await self.db.execute(
            select(Todo)
            .offset(skip)
            .limit(limit)
            .options(selectinload(Todo.tag))  # 使用 selectinload
        )
        return result.scalars().all()

    async def get_by_title(self, title: str) -> Optional[Todo]:
        result = await self.db.execute(select(Todo).where(Todo.title == title))
        return result.scalar_one_or_none()
