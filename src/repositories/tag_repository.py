from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.todo_tag import TodoTag
from src.repositories.base_repository import BaseRepository

class TagRepository(BaseRepository[TodoTag]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, TodoTag)
    
    async def get_by_name(self, name: str) -> Optional[TodoTag]:
        result = await self.db.execute(select(TodoTag).where(TodoTag.name == name))
        return result.scalar_one_or_none()
    
    async def get_by_name_ignore_case(self, name: str) -> Optional[TodoTag]:
        result = await self.db.execute(
            select(TodoTag).where(TodoTag.name.ilike(name))
        )
        return result.scalar_one_or_none()